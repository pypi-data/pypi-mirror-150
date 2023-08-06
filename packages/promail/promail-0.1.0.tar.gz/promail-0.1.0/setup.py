# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promail', 'promail.clients']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'mjml>=0.7.0,<0.8.0',
 'nox>=2022.1.7,<2023.0.0',
 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'promail',
    'version': '0.1.0',
    'description': 'The Python Email AutomatioN Framework',
    'long_description': '[![Tests](https://github.com/trafire/promail/workflows/Tests/badge.svg)](https://github.com/trafire/promail/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/trafire/promail/branch/master/graph/badge.svg)](https://codecov.io/gh/trafire/promail)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python.svg)](https://pypi.org/project/hypermodern-python/)\n# promail\n\nEmail Templates:\n\n When you install we create an email templates file with installed templates commented out. You can enable any templates by uncommenting these.\n\nEmail Templates:\n    Composed of fragments\n    Should include a json that explains format of the data and a description and a sample. We should also see if we can include a jpeg screen print of the sample data (maybe using playwright to render html and take a screen shot https://stackoverflow.com/questions/60598837/html-to-image-using-python)\n',
    'author': 'Antoine Wood',
    'author_email': 'antoinewood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trafire/promail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
