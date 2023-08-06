# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datachain_sources',
 'datachain_sources.bytes',
 'datachain_sources.files',
 'datachain_sources.query']

package_data = \
{'': ['*']}

install_requires = \
['datachain>=1.0.0,<2.0.0',
 'pandas>=2.0.2,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

extras_require = \
{'http': ['requests>=2.31.0,<3.0.0'],
 'mysql': ['sqlalchemy==1.4.46', 'mysqlclient>=2.1.1,<3.0.0'],
 'pgsql': ['sqlalchemy==1.4.46', 'psycopg2-binary>=2.9.5,<3.0.0'],
 'salesforce': ['simple-salesforce>=1.12.2,<2.0.0'],
 'sftp': ['paramiko>=3.2.0,<4.0.0'],
 'sharepoint': ['azure-common>=1.1.28,<2.0.0',
                'azure-storage-blob>=12.14.1,<13.0.0',
                'azure-storage-common>=2.1.0,<3.0.0',
                'shareplum>=0.5.1,<0.6.0'],
 'snowflake': ['sqlalchemy==1.4.46',
               'snowflake-connector-python>=2.9.0,<3.0.0',
               'snowflake-sqlalchemy>=1.4.4,<2.0.0',
               'cryptography==38.0.4']}

setup_kwargs = {
    'name': 'datachain-sources',
    'version': '0.1.3',
    'description': 'Sources for DataChain library.',
    'long_description': '',
    'author': 'Rayane AMROUCHE',
    'author_email': 'rayaneamrouche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
