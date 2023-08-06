# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegramma',
 'telegramma.api',
 'telegramma.core',
 'telegramma.modules',
 'telegramma.modules.core',
 'telegramma.modules.info',
 'telegramma.modules.lineageos',
 'telegramma.modules.nekobin',
 'telegramma.modules.sed',
 'telegramma.modules.shell',
 'telegramma.modules.speedtest',
 'telegramma.modules.translate',
 'telegramma.modules.xda']

package_data = \
{'': ['*']}

install_requires = \
['python-telegram-bot==20.0a0', 'sebaubuntu-libs>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'telegramma',
    'version': '1.0.0',
    'description': 'Modular Telegram bot',
    'long_description': '# telegramma\n\nModular Telegram bot\n\n## Installation\n\n-   Clone the repo\n-   Execute `pip3 install .` to install all the dependencies\n-   Copy `example_config.py` to `config.py`\n-   Put a bot token in `config.py`\n-   Edit additional variables in `config.py`\n\n## How to use\n\n```sh\npython3 -m telegramma\n```\n\n```\n#\n# Copyright (C) 2022 Sebastiano Barezzi\n#\n# SPDX-License-Identifier: GPL-3.0-or-later\n#\n```\n',
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/telegramma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
