# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['choc', 'choc.ddp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'loguru>=0.6.0,<0.7.0', 'pyexecjs>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'choc-ddp',
    'version': '0.1.2',
    'description': 'chocolate deduplication',
    'long_description': '# choc_ddp\n\n```python\npip install choc-ddp\n\n#推荐\npoetry add choc-ddp\n```\n\n示例\n```python\nimport asyncio \nfrom loguru import logger\nfrom choc.ddp.chocolate import Choco\n\nasync def test():\n    async with Choco() as c:\n       resp = await c.deduplication(input("待去重：\\n"),3)\n       logger.info(resp)\n       \nif __name__ == \'__main__\':\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(test())\n```',
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
