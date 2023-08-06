# keras-model-client

Python client API for the [Keras Model Server](https://gitlab.com/bgwoodward/keras-model-server-fast-api).

Install from PyPI:

```bash
pip install keras-model-client
```

Basic usage:

```python
from keras_model_client import predict

# Using Detectron2 with the default model server
result = predict('/path/to/image.jpg', 'image_queue_detectron2')

# Using YOLOv5 with a custom model server
result = predict('/path/to/image.jpg', 'image_queue_yolov5', url='http://your-model-server/predictor/')

print(result)
# PredictionResult(success=True, predictions=[...])
```

*Note:* The default model server is currently hosted at https://adamant.tator.io:8082/.

## CLI

The package provides a command-line interface invoked with `model-server-predict`. For example:

```bash
model-server-predict /path/to/image.jpg image_queue_detectron2 -f json
```

will run the image at `/path/to/image.jpg` through the Detectron2 model and format the results as JSON. Additional help is available with the `-h` or `--help` flag.

## Install from source

Clone the repository:

```bash
git clone https://github.com/kevinsbarnard/keras-model-client
cd keras-model-client
```

and install from source with Poetry:

```bash
poetry install
```

or with pip:

```bash
pip install .
```
