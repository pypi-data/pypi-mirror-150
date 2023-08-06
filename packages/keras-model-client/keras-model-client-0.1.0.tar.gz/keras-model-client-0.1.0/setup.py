# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_model_client', 'keras_model_client.scripts']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['model-server-predict = '
                     'keras_model_client.scripts.predict:main']}

setup_kwargs = {
    'name': 'keras-model-client',
    'version': '0.1.0',
    'description': 'Python client API for the Keras Model Server',
    'long_description': None,
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
