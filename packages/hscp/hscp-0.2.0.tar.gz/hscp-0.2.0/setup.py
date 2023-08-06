# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hscp']
install_requires = \
['aiohttp==3.8.1', 'requests==2.27.1']

setup_kwargs = {
    'name': 'hscp',
    'version': '0.2.0',
    'description': 'Client library for HyScores.',
    'long_description': '# HSCP\n\n## Description:\n\n**HSCP** is a [HyScores](https://github.com/0x5b/hyscores) Client, written in \nPython. Its designed to be a simple and efficient library to use in your games.\n\n## Usage:\n\n```python3\n\nfrom hscp import HyScoresClient\n\nclient = HyScoresClient(\n    # replace this with url of actually running instance of HyScores\n    url = "http://example.com",\n    # and this with name of your application\n    app = "hyscores",\n)\n\n# If you arent registered on this instance yet\nclient.register("your_login", "your_password") \n\nclient.login("your_login", "your_password")\n\n# This will get list of scores already uploaded to server\nprint(client.get_scores())\n```\n\n## License:\n\n[MIT](https://github.com/moonburnt/hscp/blob/master/LICENSE)\n',
    'author': 'moonburnt',
    'author_email': 'moonburnt@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moonburnt/hscp',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
