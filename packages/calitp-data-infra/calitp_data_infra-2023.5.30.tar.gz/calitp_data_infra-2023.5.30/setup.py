# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp_data_infra']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2.1,<3.0.0',
 'calitp-data==2023.2.15.1',
 'google-api-core>=1.31.4',
 'google-cloud-secret-manager>=1.0.0,<1.1.0',
 'humanize>=4.6.0,<5.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9,<1.10',
 'tqdm>=4.64.1,<5.0.0',
 'typing-extensions>=3.10.0.2']

setup_kwargs = {
    'name': 'calitp-data-infra',
    'version': '2023.5.30',
    'description': 'Shared code for developing data pipelines that process Cal-ITP data.',
    'long_description': 'None',
    'author': 'Andrew Vaccaro',
    'author_email': 'andrew.v@jarv.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
