# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elysium']

package_data = \
{'': ['*']}

install_requires = \
['deta>=1.1.0,<2.0.0', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'elysium',
    'version': '0.1.0',
    'description': 'Deta Base Typed ODM',
    'long_description': '#+title:🏰 Elysium\n#+author: Ian Kollipara\n#+date: <2022-05-15 Sun>\n\nElysium is a Python ODM built for [[https:deta.sh][Deta]]. The name comes from one of the mountains of Mars. The main perks being:\n- Tight integration with Deta Base\n- Lambda queries to search with\n- Your choice off dataclasses or Pydantic for data modeling\n\n\nTo install simply type:\n#+begin_src shell\npip install elysium\n#+end_src\n\nElysium is in development software, but the API is stable.\n\n** Roadmap\n- [X] Use Lambdas to query the database\n- [X] Allow use of Pydantic or dataclasses\n- [ ] Create Testing Suite\n- [ ] Implement Deta\'s updates on the backend\n- [ ] Implement some sort of way to handle related data (maybe ad-hoc joins?)\n\n** Usage\n\n#+begin_src python\nfrom elysium import Elysium\nfrom dataclasses import dataclass\n\nelysium = Elysium()\n\n@dataclass\nclass Article(Elysium.Model):\n    title: str\n    author: str\n    body: str\n\nelysium.generate_mappings()\n\n\na = Article("test", "ikollipara", "lorem ipsum")\n\nelysium.insert(a)\n\nArticle.fetch(lambda a: a.title == "test") # Article("test", "ikollipara", "lorem ipsum")\n#+end_src\n',
    'author': 'Ian Kollipara',
    'author_email': 'ian.kollipara@cune.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
