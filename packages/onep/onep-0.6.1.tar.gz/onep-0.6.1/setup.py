# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onep', 'onep.commands']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=2.9.2,<3.0.0',
 'keyring>=23.5.0,<24.0.0',
 'phonenumbers>=8.12.48,<9.0.0',
 'prettytable>=3.3.0,<4.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'validators>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['1p = onep.onep:main']}

setup_kwargs = {
    'name': 'onep',
    'version': '0.6.1',
    'description': '1Password CLI helper',
    'long_description': "# 1p - 1Password CLI helper\n\n`1p` is a wrapper around 1Password's `op` CLI tool to give a more user-friendly interface to secret retrieval.\n\nRequires Python >= 3.7.\n\nIt opens a session with 1Password and stores the session token in the system's keyring, optionally, you can run with `ONEP_SECRET_BACKEND=plain` to store it under `~/.cache/1p`.\n\nIt requires that the configured 1Password account has a shorthand defined (when using `op account add`).\n\n## Installation\n\n```shell\n$ # From PyPI\n$ pip install onep\n\n$ # Development build from GitHub\n$ https://github.com/apognu/1p/releases/download/tip/onep-tip-py3-none-any.whl\n```\n\n## Usage\n\n```shell\n$ 1p --help\nusage: 1p [-h] [-j] ACCOUNT COMMAND ...\n\npositional arguments:\n  ACCOUNT     shorthand of the 1Password account\n  COMMAND\n    signin    authenticate into a 1Password account\n    vaults    list available vaults\n    vault     show information about a vault\n    search    search entries matching provided term\n    show      display an entry\n    create    create an entry\n    edit      edit an entry\n    delete    delete an entry\n    download  download a document\n    upload    upload a document\n    share     get a shareable link to an item\n\noptions:\n  -h, --help  show this help message and exit\n  -j, --json  format output as JSON\n\n$ 1p personal search -t social\nID                            TITLE\n__________________________    GitHub\n__________________________    Twitter\n```\n\n## Item creation syntax\n\nItem creation syntax tries to determine the type of the provided values (URLs, email addresses and phone numbers), if possible. It also provides some utility to control the way values are entered and interpreted:\n\n * `field=` will set the type as `password` and prompt for the value interactively\n * `field=-` will set the type as `password` and generate a random value\n * `@field=value` will explicitely set the type as `password`\n * `+field=totpsecret` will consider the provided value as a TOTP secret key\n * `section.field=value` will create a field under a named section\n",
    'author': 'Antoine POPINEAU',
    'author_email': 'antoine@popineau.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/apognu/1p',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
