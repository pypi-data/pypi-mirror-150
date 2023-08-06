# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orx',
 'orx.impl',
 'orx.impl.gateway',
 'orx.impl.http',
 'orx.proto',
 'orx.proto.gateway',
 'orx.proto.http']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0', 'discord-typings>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'orx',
    'version': '1.0.0a0',
    'description': 'A modern, async, lightweight Discord API wrapper.',
    'long_description': "# orx\n\nA modern, async, lightweight Discord API wrapper.\n\n## Key Features\n\n- Efficient and robust ratelimit handling\n- Consistently and accurately typed\n- Provides low-level access for customisability\n\n### What Orx is **not**\n\n- A high level wrapper for people who just want a simple API wrapper, for that use discord.py or a similar fork of it.\n\n## Installing\n\n**Orx requires Python 3.10 or higher.**\n\nTo install Orx you can use:\n\n```sh\n# Linux/MacOS\npython3 -m pip install orx\n\n# Windows\npy -3 -m pip install Orx\n```\n\n## Versioning\n\nOrx is versioned according to semantic versioning with minor modifications.\n\nThe version format is `major.minor.patch`, i.e. `1.0.0`.\n\n- Major version changes may have large breaking changes to how the library works.\n- Minor version changes may have small breaking changes, for example a single method's signature changing.\n- Patch version changes should not include breaking changes.\n\nSome versions released on pypi may use the a format similar to `1.0.0a0` or `1.0.0rc0`. These are alpha and release candidate versions. It is not recommended that you use these versions in production instances of your bots.\n\n## Contributing\n\nSee [Contributing to Orx](./CONTRIBUTING.md).\n",
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/orx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
