# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beastiary',
 'beastiary.api',
 'beastiary.api.endpoints',
 'beastiary.crud',
 'beastiary.db',
 'beastiary.schemas']

package_data = \
{'': ['*'],
 'beastiary': ['webapp-dist/*', 'webapp-dist/css/*', 'webapp-dist/js/*']}

install_requires = \
['aiofiles<0.6.0', 'fastapi[all]>=0.67.0,<0.68.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['beastiary = beastiary.cli:app']}

setup_kwargs = {
    'name': 'beastiary',
    'version': '1.5.5',
    'description': '',
    'long_description': '![beastiary logo](https://beastiary.wytamma.com/images/logo.png)\n\n\n[![PyPi](https://img.shields.io/pypi/v/beastiary.svg)](https://pypi.org/project/beastiary/)\n[![tests](https://github.com/Wytamma/beastiary/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/beastiary/actions/workflows/test.yml)\n[![cov](https://codecov.io/gh/Wytamma/beastiary/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/beastiary)\n[![docs](https://github.com/Wytamma/beastiary/actions/workflows/docs.yml/badge.svg)](https://beastiary.wytamma.com/)\n\nBeastiary is designed for visualising and analysing MCMC trace files generated from Bayesian phylogenetic analyses. Beastiary works in real-time and on remote servers (e.g. a HPC). Its goal is to be a beautiful and simple yet powerful tool for Bayesian phylogenetic inference.\n\n---\n\n**Documentation**: <a href="https://beastiary.wytamma.com" target="_blank">https://beastiary.wytamma.com</a>\n\n**Source Code**: <a href="https://github.com/Wytamma/beastiaryi" target="_blank">https://github.com/Wytamma/beastiary</a>\n\n---\n\n## Installation\n```bash\npip install beastiary\n```\n\n## Use\nTo start beastiary use the `beastiary` command. \n\n```bash\nbeastiary\n```\n\n![](https://beastiary.wytamma.com/images/screen_shot_dark.png)\n\nFor more information read the [docs](https://beastiary.wytamma.com/).\n',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
