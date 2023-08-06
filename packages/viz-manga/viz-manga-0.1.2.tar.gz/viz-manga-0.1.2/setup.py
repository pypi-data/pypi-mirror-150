# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viz_manga']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'viz-image-unobfuscate>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'viz-manga',
    'version': '0.1.2',
    'description': 'Viz Manga Reader',
    'long_description': '# Viz Manga Viewer\nRetrieves and unobfuscates manga pages for an input chapter id. Manga pages can be saves the dual spread images as well as single page images. Chapter ids need to be retrieved from the Viz site by looking at the chapter url.\n\nDISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only. Please delete the retrieved pages after reading.\n\n# Installation\n```\npip install viz_manga\n```\n\n# CLI Usage\n```\nusage: manga_fetch.py [-h] [--directory DIRECTORY] [--combine] chapter_id\n\nUnobfuscates an entire manga chapter for reading.\n\npositional arguments:\n  chapter_id            Chapter id obtained from the Viz site.\n\noptions:\n  -h, --help            show this help message and exit\n  --directory DIRECTORY\n                        Output directory to save the unobfuscated pages.\n  --combine             Combine left and right pages into one image.\n```\n\n## Example\n```\n>>> python manga_fetch.py 24297 --directory images/ --combine\n\nINFO:root:Getting 20 pages for One Piece Chapter 1047.0\nSuccessfully retrieved chapter 24297\n\n```\n\n# Docker\n```\n>>> docker build -t viz-manga .\n>>> docker run -v /home/user/images/:/app/images viz-manga  24297 --directory images/ --combine\n\nINFO:root:Getting 20 pages for One Piece Chapter 1047.0\nSuccessfully retrieved chapter 24297\n\n```\n\n# Series and Chapter metadata\nAdditionally bundled are scripts to lookup the chapter ids for the fecthing script. The manga details script requires a series slug to lookup available (free) chapters.\n\n## CLI Options\n```\nusage: manga_details.py [-h] {series,chapters} ...\n\nLookup Viz managa information.\n\npositional arguments:\n  {series,chapters}\n    series           Get series title and slug (for chapter lookup) obtained from the Viz site.\n    chapters         Get chapter title and id obtained from the Viz site.\n\noptions:\n  -h, --help         show this help message and exit\n```\n\n## Lookup Manga Series\n```\n>>> python manga_details.py series\n\n{\'name\': \'7thGARDEN\', \'slug\': \'7th-garden\'}\n{\'name\': \'Agravity Boys\', \'slug\': \'agravity-boys\'}\n{\'name\': \'Akane-banashi\', \'slug\': \'akane-banashi\'}\n{\'name\': "Akira Toriyama\'s Manga Theater", \'slug\': \'akira-toriyamas-manga-theater\'}\n{\'name\': \'All You Need is Kill\', \'slug\': \'all-you-need-is-kill-manga\'}\n{\'name\': \'Assassination Classroom\', \'slug\': \'assassination-classroom\'}\n\n```\n\n## Lookup Manga Chapters\n```\n>>> python manga_details.py chapters 7th-garden\n\n{\'title\': \'ch-1\', \'id\': \'15220\', \'link\': \'https://www.viz.com/shonenjump/7th-garden-chapter-1/chapter/15220\', \'is_free\': True}\n{\'title\': \'ch-2\', \'id\': \'15221\', \'link\': \'https://www.viz.com/shonenjump/7th-garden-chapter-2/chapter/15221\', \'is_free\': True}\n{\'title\': \'ch-3\', \'id\': \'15222\', \'link\': \'https://www.viz.com/shonenjump/7th-garden-chapter-3/chapter/15222\', \'is_free\': True}\n{\'title\': \'ch-4\', \'id\': \'15223\', \'link\': \'https://www.viz.com/shonenjump/7th-garden-chapter-4/chapter/15223\', \'is_free\': False}\n{\'title\': \'ch-5\', \'id\': \'15224\', \'link\': \'https://www.viz.com/shonenjump/7th-garden-chapter-5/chapter/15224\', \'is_free\': False}\n\n```\n\n### Get Manga Chapter\n```\n>>> python manga_fetch.py 15220 --directory images/ --combine\n\nINFO:root:Getting 79 pages for Root 1: The Demon\'s Servant\nSuccessfully retrieved chapter 15220\n\n```',
    'author': 'Kevin Ramdath',
    'author_email': 'krpent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minormending/viz-manga',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
