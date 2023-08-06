# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wekan_logstash']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.4,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pymongo>=4.1.1,<5.0.0',
 'python-slugify>=6.1.2,<7.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['get_cards = wekan_logstash.cli:cli']}

setup_kwargs = {
    'name': 'wekan-logstash',
    'version': '0.1.0',
    'description': 'Simple script that will print cards data for logstash (ELK Kibana) in JSON format',
    'long_description': '# wekan-logstash\n\nTo format data for logstash and ELK (Kibana) - Format below :\n\n```json\n{\n  "id": "7WfoXMKnmbtaEwTnn",\n  "title": "Card title",\n  "storyPoint": 2.0,\n  "nbComments": 1,\n  "createdBy": "fmonthel",\n  "labels": [\n    "I-U",\n    "I-Nu"\n  ],\n  "assignees": "fmonthel",\n  "members": [\n    "fmonthel",\n    "Olivier"\n  ],\n  "boardSlug": "test",\n  "description": "A subtask description",\n  "startAt": "2021-06-07T20:36:00.000Z",\n  "endAt": "2021-06-07T20:36:00.000Z",\n  "requestedBy": "LR",\n  "assignedBy": "MM",\n  "receivedAt": "2021-06-07T20:36:00.000Z",\n  "archivedAt": "2021-06-07T20:36:00.000Z",\n  "createdAt": "2021-06-07T20:36:00.000Z",\n  "lastModification": "2017-02-19T03:12:13.740Z",\n  "list": "Done",\n  "dailyEvents": 5,\n  "board": "Test",\n  "isArchived": true,\n  "dueAt": "2021-06-07T20:36:00.000Z",\n  "swimlaneTitle": "Swinline Title",\n  "customfieldName1": "value1",\n  "customfieldName2": "value2",\n  "boardId": "eJPAgty3guECZf4hs",\n  "cardUrl": "http://localhost/b/xxQ4HBqsmCuP5mYkb/semanal-te/WufsAmiKmmiSmXr9m",\n  "checklists": [\n      {"TODO": [\n          {"isfinished": false, "title": "todo1"},\n          {"isfinished": false, "title": "todo2"}\n        ]\n      },\n      {"DONE": [\n          {"isfinished": true, "title": "done1"},\n          {"isfinished": true, "title": "done2"}\n        ]\n      }\n  ]\n}\n```\n\nGoal is to export data into Json format that we can be used as input for Logstash and ElastisSearch / Kibana (ELK)\n\nImport in logstash should be done daily basic (as we have field daily event)\n',
    'author': 'Franklin Gomez',
    'author_email': 'fgomezotero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fgomezotero/wekan-logstash',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
