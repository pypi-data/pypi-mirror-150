# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acquisition_decisions_sc',
 'acquisition_decisions_sc.annex',
 'acquisition_decisions_sc.field',
 'acquisition_decisions_sc.ponencia']

package_data = \
{'': ['*']}

install_requires = \
['acquisition-case-transform>=0.1.1,<0.2.0',
 'acquisition-ruling-phrase>=0.3.1,<0.4.0',
 'acquisition-sanitizer>=0.4.1,<0.5.0',
 'httpx>=0.22,<0.23']

setup_kwargs = {
    'name': 'acquisition-decisions-sc',
    'version': '0.0.2',
    'description': "Processes decisions starting 1996 to present date. The Philippine Supreme Court's digital library starts in 1996.",
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
