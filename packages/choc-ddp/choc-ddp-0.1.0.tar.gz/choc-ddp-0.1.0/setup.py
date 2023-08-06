# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'loguru>=0.6.0,<0.7.0', 'pyexecjs>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'choc-ddp',
    'version': '0.1.0',
    'description': 'chocolate deduplication',
    'long_description': '# choco_ddp\n',
    'author': 'AnjoyLi',
    'author_email': '1589631311@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
