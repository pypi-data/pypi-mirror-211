# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['driftpy', 'driftpy.constants', 'driftpy.idl', 'driftpy.math', 'driftpy.setup']

package_data = \
{'': ['*']}

install_requires = \
['aiodns==3.0.0',
 'aiohttp==3.8.3',
 'aiosignal==1.3.1',
 'anchorpy-core==0.1.2',
 'anchorpy==0.10.0',
 'anyio==3.6.2',
 'apischema==0.17.5',
 'async-timeout==4.0.2',
 'attrs==22.1.0',
 'backoff==2.2.1',
 'base58==2.1.1',
 'based58==0.1.1',
 'borsh-construct==0.1.0',
 'cachetools==4.2.4',
 'certifi==2022.12.7',
 'cffi==1.15.1',
 'charset-normalizer==2.1.1',
 'construct-typing==0.5.3',
 'construct==2.10.68',
 'dnspython==2.2.1',
 'exceptiongroup==1.0.4',
 'flake8==6.0.0',
 'frozenlist==1.3.3',
 'h11==0.14.0',
 'httpcore==0.16.3',
 'httpx==0.23.1',
 'idna==3.4',
 'iniconfig==1.1.1',
 'jsonalias==0.1.1',
 'jsonrpcclient==4.0.2',
 'jsonrpcserver==5.0.9',
 'jsonschema==4.17.3',
 'loguru==0.6.0',
 'mccabe==0.7.0',
 'mkdocs>=1.3.0,<2.0.0',
 'more-itertools==8.14.0',
 'multidict==6.0.3',
 'oslash==0.6.3',
 'packaging==22.0',
 'pluggy==1.0.0',
 'psutil==5.9.4',
 'py==1.11.0',
 'pycares==4.3.0',
 'pycodestyle==2.10.0',
 'pycparser==2.21',
 'pyflakes==3.0.1',
 'pyheck==0.1.5',
 'pyrsistent==0.19.2',
 'pytest-asyncio==0.17.2',
 'pytest-xprocess==0.18.1',
 'pytest==6.2.5',
 'pythclient==0.1.4',
 'requests==2.28.1',
 'rfc3986==1.5.0',
 'sniffio==1.3.0',
 'solana==0.25.1',
 'solders==0.2.0',
 'sumtypes==0.1a6',
 'toml==0.10.2',
 'tomli==2.0.1',
 'toolz==0.11.2',
 'types-cachetools==4.2.10',
 'types-requests>=2.28.9,<3.0.0',
 'typing-extensions==4.4.0',
 'urllib3==1.26.13',
 'websockets==10.4',
 'yarl==1.8.2',
 'zstandard==0.17.0']

setup_kwargs = {
    'name': 'driftpy',
    'version': '0.6.37',
    'description': 'A Python client for the Drift DEX',
    'long_description': '# DriftPy\n\n<div align="center">\n    <img src="docs/img/drift.png" width="30%" height="30%">\n</div>\n\nDriftPy is the Python client for the [Drift](https://www.drift.trade/) protocol. It allows you to trade and fetch data from Drift using Python.\n\n**[Read the full SDK documentation here!](https://drift-labs.github.io/driftpy/)**\n\n## Installation\n\n```\npip install driftpy\n```\n\nNote: requires Python >= 3.10.\n\n## SDK Examples\n\n- `examples/` folder includes more examples of how to use the SDK including how to provide liquidity/become an lp, stake in the insurance fund, etc.\n\n## Setting Up Dev Env\n\n`bash setup.sh`\n\n\n## Building the docs\n\nLocal Docs: `mkdocs serve`\n\nUpdating public docs: `poetry run mkdocs gh-deploy --force`\n\n## Releasing a new version of the package\n\n- `python new_release.py`\n- Create a new release at https://github.com/drift-labs/driftpy/releases.\n  - (The CI process will upload a new version of the package to PyPI.)\n\n# Development\n\nEnsure correct python version (using pyenv is recommended):\n```\npyenv install 3.10.11\npyenv global 3.10.11\npoetry env use $(pyenv which python)\n```\n\nInstall dependencies:\n```\npoetry install\n```\n\nRun tests:\n```\npoetry run bash test.sh\n```\n\nRun Acceptance Tests\n```\npoetry run bash acceptance_test.sh\n```',
    'author': 'x19',
    'author_email': 'https://twitter.com/0xNineteen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drift-labs/driftpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
