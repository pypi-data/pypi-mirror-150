# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asgikit', 'asgikit.errors', 'asgikit.multipart']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgikit',
    'version': '0.1.1',
    'description': 'Toolkit for building ASGI applications and libraries',
    'long_description': '# Asgikit - ASGI Toolkit\n\nAsgikit is a toolkit for building asgi applications and frameworks.\n\nIt is intended to be a minimal library and provide the building blocks for other libraries.\n\n## Features:\n\n- Request\n  - Headers\n  - Cookies\n  - Body (bytes, str, json)\n  - Form\n    - url encoded\n    - multipart\n- Response\n  - Plain text\n  - Json\n  - Streaming\n  - File\n- Websockets\n\n## Example\n\n```python\nfrom asgikit.requests import HttpRequest\nfrom asgikit.responses import JsonResponse\n\nasync def main(scope, receive, send):\n    request = HttpRequest(scope, receive, send)\n    body = await request.json()\n    data = {"lang": "Python", "async": True}\n    response = JsonResponse(content=data)\n    await response(scope, receive, send)\n```',
    'author': 'Livio Ribeiro',
    'author_email': 'livioribeiro@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/livioribeiro/asgikit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
