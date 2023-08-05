# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latch_asgi']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2.6.0,<3.0.0',
 'hypercorn[uvloop]>=0.14.3,<0.15.0',
 'latch-config>=0.1.6,<0.2.0',
 'latch-data-validation>=0.1.3,<0.2.0',
 'latch-o11y>=0.1.4,<0.2.0',
 'opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-instrumentation-asgi>=0.36b0,<0.37',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'orjson>=3.8.5,<4.0.0',
 'pysimdjson>=5.0.2,<6.0.0']

setup_kwargs = {
    'name': 'latch-asgi',
    'version': '0.1.1',
    'description': 'ASGI python server',
    'long_description': '# python-asgi\n',
    'author': 'Max Smolin',
    'author_email': 'max@latch.bio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
