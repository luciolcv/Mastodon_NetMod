"""
Mastodon NetMod - A Mastodon Network Moderation Tool
------------------------------------------------------------------------------------------------------
A tool for collecting and analyzing Mastodon network moderation data using the official Mastodon APIs.

Created by: Lucio La Cava
Created on: Late 2024
Version: 0.0.1
License: Apache 2.0

This tool discovers Mastodon instances using the instances.social API, fetches their blocklists,
and stores them in MongoDB for analysis.

Before running the tool, please set your instances.social API key and 
configure the MongoDB connection parameters in the config.json file.

Usage:
python net_mod_tool.py
"""

# Libraries
import requests
from multiprocessing.pool import ThreadPool as Pool
from tqdm import tqdm
from pymongo import MongoClient
from datetime import datetime
from pymongo import MongoClient
from typing import List, Optional
import logging
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("net_mod_tool")

# Add global config variable
config = None

# Functions
def load_config(config_path: str = "config.json") -> dict:
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to config file
        
    Returns:
        dict: Configuration parameters
    """
    global config
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def get_current_instances() -> Optional[List[str]]:
    """
    Retrieves the list of known Mastodon instances from instances.social platform.

    Returns:
        Optional[List[str]]: List of instance names or None if the request fails
    """
    try:
        INSTANCES_SOCIAL_API = config['api_key']
        INSTANCES_SOCIAL_URL = config['api_url']
        INSTANCES_SOCIAL_HEADER = {"Authorization": "Bearer " + INSTANCES_SOCIAL_API}
        API_PARAMS = config['api_params']
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise

    try:
        logger.info(f"Fetching instances with min {API_PARAMS['min_active_users']} active users and version >= {API_PARAMS['min_version']}...")
        response = requests.get(
            url=INSTANCES_SOCIAL_URL,
            headers=INSTANCES_SOCIAL_HEADER,
            timeout=30,
            params=API_PARAMS
        )
        response.raise_for_status()

        instances_list = response.json()['instances']
        logger.info(f"Instances found: {len(instances_list)}")
        return [elem['name'] for elem in instances_list]

    except requests.RequestException as e:
        logger.error(f"Error fetching instances: {e}")
        return None


def get_blocklist_from_instance(instance: str) -> Optional[List[dict]]:
    """
    Retrieves the blocklist of a given instance.

    Args:
        instance (str): The instance domain name

    Returns:
        Optional[List[dict]]: List of blocking rules or None if request fails
    """
    blocklist_url = f"https://{instance}/api/v1/instance/domain_blocks"

    try:
        # Verify content type first
        response_head = requests.head(
            url=blocklist_url,
            headers=config['headers'],
            timeout=(5, 5)
        )
        if 'application/json' not in response_head.headers.get('content-type', ''):
            return None

        response = requests.get(
            url=blocklist_url,
            headers=config['headers'],
            timeout=(5, 5)
        )
        response.raise_for_status()

        items = response.json()
        return [{
            'instance': instance,
            'blocked_domain': i.get('domain'),
            'severity': i.get('severity'),
            'comment': i.get('comment'),
            'timestamp': datetime.now().strftime("%Y-%m-%d")
        } for i in items]

    except requests.RequestException as e:
        logger.debug(f"Error fetching blocklist from {instance}: {e}")
        return None


def chunkify(data, size):
    """
    This function splits a list into chunks of a given size for parallel processing.
    """
    for i in range(0, len(data), size):
        yield data[i:i+size]


def crawl_blocklist(N_PROCESSES=8, CHUNK_SIZE=1000):
    """
    This function crawls the blocklists from all instances known to the instances.social platform.
    """
    print(f"\nStarting blocklist crawling with {N_PROCESSES} processes...")
    # Getting the list of instances
    known_instances = get_current_instances()
    if not known_instances:
        print("Error: Failed to fetch instances list")
        return []

    logger.info(f"Processing {len(known_instances)} instances in chunks of {CHUNK_SIZE}...")
    # Parallelized execution
    pool = Pool(N_PROCESSES)

    # Results
    results = []

    # Chunks
    chunks = list(chunkify(known_instances, CHUNK_SIZE))
    logger.info(f"Extracted {len(chunks)} chunks")

    # Executing
    for chunk in tqdm(chunks):
        pbar = tqdm(desc=f"Extracting blocklists", total=len(chunk))
        for res in pool.imap_unordered(get_blocklist_from_instance, chunk):
            if res is not None:
                results.extend(res)
            pbar.set_description(
                f"Blocked domains: {len(results)} | Instances processed")
            pbar.update()
        pbar.close()

    logger.info(f"Valid blocklists: {len(results)}")

    return results


def store_blocklists_to_mongo(blocklists: List[dict]) -> None:
    """
    Stores the blocklists to a MongoDB database using connection parameters from config.

    Args:
        blocklists (List[dict]): List of blocking rules to store
    """
    logger.info(f"Connecting to MongoDB to store {len(blocklists)} blocklist entries...")

    try:
        mongodb_config = config.get('mongodb', {})
        client = MongoClient(
            host=mongodb_config.get('host', 'localhost'),
            port=mongodb_config.get('port', 27017)
        )
        db = client[mongodb_config.get('db_name', None)]
        collection = db[mongodb_config.get('collection_name', None)]
  
        inserted_count = 0
        try:
            result = collection.insert_many(blocklists, ordered=False)
            inserted_count = len(result.inserted_ids)
            logger.info(f"Inserted {inserted_count} out of {len(blocklists)} documents!")
        except Exception as e:
            logger.error(f"{len(blocklists) - inserted_count} documents were not inserted.")

    except Exception as e:
        logger.error(f"Error storing to MongoDB: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    load_config()
    blocklists = crawl_blocklist()
    store_blocklists_to_mongo(blocklists)
