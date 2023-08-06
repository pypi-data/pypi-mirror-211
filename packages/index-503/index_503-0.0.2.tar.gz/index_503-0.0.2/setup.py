# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['index_503']

package_data = \
{'': ['*']}

install_requires = \
['airium>=0.2.5,<0.3.0',
 'click>=8.1.3,<9.0.0',
 'consolekit>=1.4.1,<2.0.0',
 'dist-meta>=0.8.0,<0.9.0',
 'natsort>=8.3.1,<9.0.0',
 'yarl>=1.9.2,<2.0.0']

entry_points = \
{'console_scripts': ['index-503 = index_503.main:main_cli']}

setup_kwargs = {
    'name': 'index-503',
    'version': '0.0.2',
    'description': 'PEP 503 index builder',
    'long_description': '# Index 503\n\n<p align="center">\n  <a href="https://github.com/bdraco/index-503/actions/workflows/ci.yml?query=branch%3Amain">\n    <img src="https://img.shields.io/github/actions/workflow/status/bdraco/index-503/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://index-503.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/index-503.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/bdraco/index-503">\n    <img src="https://img.shields.io/codecov/c/github/bdraco/index-503.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/index-503/">\n    <img src="https://img.shields.io/pypi/v/index-503.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/index-503.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/index-503.svg?style=flat-square" alt="License">\n</p>\n\nPEP 503 index builder\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install index-503`\n\n## Credits\n\nThis package was created with\n[Copier](https://copier.readthedocs.io/) and the\n[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)\nproject template.\n\nThis project borrows heavily from Dominic Davis-Foster\'s simple503 https://github.com/repo-helper/simple503\n',
    'author': 'J. Nick Koston',
    'author_email': 'nick@koston.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bdraco/index-503',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
