# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['e621_dl']
install_requires = \
['e621-temp>=1.0.7,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['e6 = e621_dl:app']}

setup_kwargs = {
    'name': 'e621-dl',
    'version': '2.2.3',
    'description': 'A simple and fast e621 post/pool downloader',
    'long_description': '# e621-dl\n**e621-dl** is a simple and fast e621 post/pool downloader. It is based upon the [e621](https://github.com/PatriotRossii/e621-py) api wrapper both in implementation and interface.\n\n## Installation\n`pip install e621-dl`\n\n## Quickstart\n### Downloading Posts\n* To download posts with the ids 12345 and 67891:\n`e6 posts get 12345 67891`\n* To download all posts that match the canine but not the 3d tag:\n`e6 posts search "canine -3d"`\n* To download 500 posts that match the 3d tag:\n`e6 posts search 3d -m 500`\n* To download posts that match the 3d tag to directory e621_downloads:\n`e6 posts search 3d -d e621_downloads`\n* To download all posts that match the 3d tag and replace all post duplicates from the parent directory with symlinks:\n`e6 posts search 3d -s`\n\n### Downloading Pools\n* To download the pools with the ids 12345 and 67891:\n`e6 pools get 12345 67891`\n* To download at most 10 pools whose names start with "Hello" and end with "Kitty" with anything else in the middle.\n`e6 pools search --name-matches Hello*Kitty -m 10`\n* To download the top 3 active series ordered by post count to a directory named "my_top_3":\n`e6 pools search --is-active --order post_count -m 3 -d my_top_3`\n* There are a lot more options so I recommend checking out the output of `e6 pools search --help`\n### Using Api Key\n* To save e621 login information to be used for every future query:\n`e6 login`\n* To remove e621 login information:\n`e6 logout`\n\n### Optimizing Space\n* To replace all post duplicates from the current directory (all of its subdirectories) with symlinks:\n`e6 clean`\n\n## FAQ and Known Issues\n* If your tags include the minus (-) sign, a colon (:), or any other character bash/typer might consider special -- you must wrap your query in quotation marks. For example,\n`e6 posts search "3d -canine order:score"`\n* For advanced reference, use `--help` option. For example, `e6 --help`, `e6 posts search --help`, etc.\n',
    'author': 'HMiku8338',
    'author_email': 'hmiku8338@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmiku8338/e621-dl',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
