# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shared_dependencies']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'asttokens>=2.1.0,<3.0.0',
 'colorama>=0.4.6,<0.5.0',
 'cryptography>=40.0.2,<41.0.0',
 'executing>=1.2.0,<2.0.0',
 'httpx>=0.24.0,<0.25.0',
 'pure-eval>=0.2.2,<0.3.0',
 'pycryptodome>=3.15.0,<4.0.0',
 'pydantic[dotenv]>=1.10.2,<2.0.0',
 'redis>=4.3.5,<5.0.0',
 'sentry-sdk>=1.11.0,<2.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'shared-dependencies',
    'version': '1.2.1',
    'description': '',
    'long_description': 'None',
    'author': 'Jean-Charles Bouchaud',
    'author_email': 'jeancharles-b@evidenceb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
