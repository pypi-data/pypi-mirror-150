# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adviceslip']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

extras_require = \
{'cli': ['typer>=0.4.1,<0.5.0']}

entry_points = \
{'console_scripts': ['adviceslip = adviceslip.cli:app']}

setup_kwargs = {
    'name': 'adviceslip',
    'version': '1.0.1',
    'description': 'Client for the Advice Slip API',
    'long_description': None,
    'author': 'cobaltgit',
    'author_email': 'criterion@chitco.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
