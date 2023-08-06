"""
API operations.
"""


from pathlib import Path
from typing import Union

import requests

from keras_model_client.lib.models import PredictionResult


SESSION = requests.Session()


def predict(
    image_path: Union[str, Path], model_type: str, url: str
) -> PredictionResult:
    """
    Run an image through the model server and return the result on success.
    """
    image_path = Path(image_path)

    with image_path.open('rb') as f:
        response = SESSION.post(url, data={'model_type': model_type}, files={'file': f})

    response.raise_for_status()

    result = PredictionResult.from_json(response.content)
    return result
