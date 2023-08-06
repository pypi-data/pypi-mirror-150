# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pixelbin', 'pixelbin.common', 'pixelbin.platform', 'pixelbin.platform.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'marshmallow>=3.15.0,<4.0.0',
 'pytz>=2022.1,<2023.0',
 'ujson>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'pixelbin',
    'version': '1.0.1',
    'description': 'Pixelbin SDK for Python',
    'long_description': '# Pixelbin Backend SDK for Python\n\nPixelbin Backend SDK for python helps you integrate the core Pixelbin features with your application.\n\n## Getting Started\n\nGetting started with Pixelbin Backend SDK for Python\n\n### Installation\n\n```\npip install pixelbin\n```\n\n---\n\n### Usage\n\n#### Quick Example\n\n```python\nimport asyncio\n\nfrom pixelbin import PixelbinClient, PixelbinConfig\n\n// create client with your API_TOKEN\nconfig = PixelbinConfig({\n    "domain": "https://api.pixelbin.io",\n    "apiSecret": "API_TOKEN",\n})\n\n// Create a pixelbin instance\npixelbin:PixelbinClient = PixelbinClient(config=config)\n\n# Sync method call\ntry:\n    result = pixelbin.assets.listFiles()\n    print(result)\nexcept Exception as e:\n    print(e)\n\n# Async method call\ntry:\n    result = asyncio.get_event_loop().run_until_complete(pixelbin.assets.listFilesAsync())\n    print(result)\nexcept Exception as e:\n    print(e)\n```\n\n## Documentation\n\n-   [API docs](documentation/platform/README.md)\n',
    'author': 'Pixelbin',
    'author_email': 'dev@pixelbin.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pixelbin-dev/pixelbin-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
