# Mastodon_NetMod 🐘 🔍 

<img src="netmod_logo.jpeg" alt="Mastodon_NetMod" width="250"/>


**Mastodon_NetMod** is an under-development Python toolkit for working with [Mastodon](https://joinmastodon.org/) network moderation data.
It leverages the [Official Mastodon APIs](https://docs.joinmastodon.org/) to provide easy-to-use access to publicly available Mastodon network moderation events.

**Mastodon_NetMod** only relies on the *publicly accessible* endpoints from Mastodon and does not require any authentication to access public data.

**Mastodon_NetMod** is a work-in-progress toolkit, that currently supports the following operations:
- [x]   Fetching of currently online Mastodon instances from the instances.social platform
- [X]   Collection of network moderation events (i.e., blocks) among Mastodon instances
- [x]   Export into DBs of the collected events

---

### How to use?
- Obtain a token from the [instances.social](https://instances.social/api/token) platform to access the list of tracked instances
- Update the *config.json* file according to your information
- Run and enjoy! :)
---

If you find this repo useful, please cite our work:
```latex

@inproceedings{LaCava2024polarization,
  author = {{La Cava}, Lucio and Mandaglio, Domenico and Tagarelli, Andrea},
  title = {Polarization in Decentralized Online Social Networks},
  year = {2024},
  doi = {10.1145/3614419.3644013},
  booktitle = {Proceedings of the 16th ACM Web Science Conference},
  series = {WebSci '24}
}

@inproceedings{Bono2024decentralizedmoderation,
  author = {Bono, Carlo Alberto and La Cava, Lucio and Luceri, Luca and Pierri, Francesco},
  title = {An Exploration of Decentralized Moderation on Mastodon},
  year = {2024},
  isbn = {9798400703348},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  doi = {10.1145/3614419.3644016},
  booktitle = {Proceedings of the 16th ACM Web Science Conference},
  pages = {53–58},
  numpages = {6},
  series = {WEBSCI '24}
}

@article{LaCava2023SciRep,
  author = {La Cava, Lucio and Aiello, Luca Maria and Tagarelli, Andrea},
  date = {2023/12/07},
  doi = {10.1038/s41598-023-48200-7},
  id = {Cava2023},
  isbn = {2045-2322},
  journal = {Scientific Reports},
  number = {1},
  pages = {21626},
  title = {Drivers of social influence in the Twitter migration to Mastodon},
  volume = {13},
  year = {2023}
}

@article{LaCava2022OSNEM,
  title = {Information consumption and boundary spanning in Decentralized Online Social Networks: The case of Mastodon users},
  journal = {Online Social Networks and Media},
  volume = {30},
  pages = {100220},
  year = {2022},
  issn = {2468-6964},
  doi = {10.1016/j.osnem.2022.100220},
  author = {{La Cava}, Lucio and Greco, Sergio and Tagarelli, Andrea}
}

@article{LaCava2022ICWSM,
  title = {Network Analysis of the Information Consumption-Production Dichotomy in Mastodon User Behaviors},
  volume = {16},
  doi = {10.1609/icwsm.v16i1.19391},
  number = {1},
  journal = {Proceedings of the International AAAI Conference on Web and Social Media},
  author = {La Cava, Lucio and Greco, Sergio and Tagarelli, Andrea},
  year = {2022},
  month = may,
  pages = {1378-1382},
  html = https://ojs.aaai.org/index.php/icwsm/article/view/19391
}

@article{LaCava2021APNS,
  author = {La Cava, Lucio and Greco, Sergio and Tagarelli, Andrea},
  date = {2021/09/01},
  doi = {10.1007/s41109-021-00392-5},
  isbn = {2364-8228},
  journal = {Applied Network Science},
  number = {1},
  pages = {64},
  title = {Understanding the growth of the Fediverse through the lens of Mastodon},
  url = {https://doi.org/10.1007/s41109-021-00392-5},
  volume = {6},
  year = {2021}
}
```


---

🚨 **This code repository is made available for research and informational purposes only!**

*The authors hereby declare that they are not responsible for any harmful or objectionable usage of Mastodonte. \
By accessing and using this code repository, users acknowledge and accept this disclaimer.*






