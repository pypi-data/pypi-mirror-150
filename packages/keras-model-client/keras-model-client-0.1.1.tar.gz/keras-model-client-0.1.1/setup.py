# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_model_client', 'keras_model_client.lib', 'keras_model_client.scripts']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['model-server-predict = '
                     'keras_model_client.scripts.predict:main']}

setup_kwargs = {
    'name': 'keras-model-client',
    'version': '0.1.1',
    'description': 'Python client API for the Keras Model Server',
    'long_description': "# keras-model-client\n\nPython client API for the [Keras Model Server](https://gitlab.com/bgwoodward/keras-model-server-fast-api).\n\nInstall from PyPI:\n\n```bash\npip install keras-model-client\n```\n\nBasic usage:\n\n```python\nfrom keras_model_client import predict\n\n# Using Detectron2 with the default model server\nresult = predict('/path/to/image.jpg', 'image_queue_detectron2')\n\n# Using YOLOv5 with a custom model server\nresult = predict('/path/to/image.jpg', 'image_queue_yolov5', url='http://your-model-server/predictor/')\n\nprint(result)\n# PredictionResult(success=True, predictions=[...])\n```\n\n*Note:* The default model server is currently hosted at https://adamant.tator.io:8082/.\n\n## CLI\n\nThe package provides a command-line interface invoked with `model-server-predict`. For example:\n\n```bash\nmodel-server-predict /path/to/image.jpg image_queue_detectron2 -f json\n```\n\nwill run the image at `/path/to/image.jpg` through the Detectron2 model and format the results as JSON. Additional help is available with the `-h` or `--help` flag.\n\n## Install from source\n\nClone the repository:\n\n```bash\ngit clone https://github.com/kevinsbarnard/keras-model-client\ncd keras-model-client\n```\n\nand install from source with Poetry:\n\n```bash\npoetry install\n```\n\nor with pip:\n\n```bash\npip install .\n```\n",
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
