# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['digdaglog2sql']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'taskipy>=1.10.1,<2.0.0', 'tdworkflow>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['digdaglog2sql = digdaglog2sql.cli:run']}

setup_kwargs = {
    'name': 'digdaglog2sql',
    'version': '0.0.2',
    'description': 'Extract SQLs from digdag log',
    'long_description': '# digdaglog2sql\n\n## Install\n\n```sh\npip install --user digdaglog2sql\n```\n\nor,\n\n```sh\n$ python -m venv .venv\n$ source .venv/bin/activate\n(.venv)$ pip install digdaglog2sql\n```\n\n## Usage\n\n```sh\n$ digdaglog2sql --help\nUsage: digdaglog2sql [OPTIONS]\n\nOptions:\n  --input FILENAME               Option is mutually exclusive with session_id,\n                                 site.\n  --session-id INTEGER           Session ID of workflow. Option is mutually\n                                 exclusive with input.\n  --site [us|jp|eu01|ap02|ap03]  Option is mutually exclusive with input.\n  --output FILENAME              [required]\n  --drop-cdp-db                  If true, drop cdp_audience_xxx DB name.\n  --help                         Show this message and exit.\n```\n\nYou can use log file on local environment.\n\n```sh\ndigdaglog2sql --input workflow-log.txt --output output.sql\n```\n\nOr, you can use Session ID of Treasure Workflow.\n\n```sh\ndigdaglog2sql --session-id 12345 --site us --output output.sql\n```\n\nEnsure set `TD_API_KEY` into environment variable.\n\n## Note\n\nAs of May 5 2022, if you want to use sqllineage for Trino and Hive logs from Treasure Data,\nrecommend to install sqlparse and sqllineage as the following:\n\n```sh\npip install git+https://github.com/chezou/sqlparse.git@trino#egg=sqlparse==0.4.3.dev0\npip install git+https://github.com/chezou/sqllineage.git@trino#egg=sqllineage==1.3.4\n```\n\nYou have to ensure to have node environment for sqllineage installation from source.\n',
    'author': 'Aki Ariga',
    'author_email': 'chezou@gmail.com',
    'maintainer': 'Aki Ariga',
    'maintainer_email': 'chezou@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
