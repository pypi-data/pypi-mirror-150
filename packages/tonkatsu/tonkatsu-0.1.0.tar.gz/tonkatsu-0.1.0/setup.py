# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonkatsu']

package_data = \
{'': ['*']}

modules = \
['__init__', 'py']
install_requires = \
['aiohttp>=3.8.1,<4.0.0']

extras_require = \
{'docs': ['sphinx>=4.0.0,<5.0.0', 'sphinxcontrib-trio', 'furo']}

setup_kwargs = {
    'name': 'tonkatsu',
    'version': '0.1.0',
    'description': 'An asynchronous and lightweight wrapper around the anilist GraphQL API',
    'long_description': '<div align="center">\n    <h1><a href="https://jisho.org/word/%E8%B1%9A%E3%82%AB%E3%83%84" />Tonkatsu 『豚カツ』</h1>\n    <a href=\'https://github.com/AbstractUmbra/tonkatsu/actions/workflows/build.yaml\'>\n        <img src=\'https://github.com/AbstractUmbra/tonkatsu/actions/workflows/build.yaml/badge.svg\' alt=\'Build status\' />\n    </a>\n    <a href=\'https://github.com/AbstractUmbra/tonkatsu/actions/workflows/coverage_and_lint.yaml\'>\n        <img src=\'https://github.com/AbstractUmbra/tonkatsu/actions/workflows/coverage_and_lint.yaml/badge.svg\' alt=\'Linting and Typechecking\' />\n    </a>\n</div>\n<div align="center">\n    <a href=\'https://tonkatsu.readthedocs.io/en/latest/?badge=latest\'>\n        <img src=\'https://readthedocs.org/projects/tonkatsu/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n</div>\n<h1></h1>\n<br>\n\nA lightweight and asynchronous wrapper around the [Anilist GraphQL API](...).\n\nYou can see our stable docs [here](https://tonkatsu.readthedocs.io/en/stable/)!\n',
    'author': 'Alex Nørgaard',
    'author_email': 'Umbra@AbstractUmbra.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AbstractUmbra/tonkatsu',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
