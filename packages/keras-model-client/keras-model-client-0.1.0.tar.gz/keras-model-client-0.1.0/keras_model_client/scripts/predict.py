"""
Run an image through the model server and output the reults.
"""


import argparse
from pathlib import Path
import sys
from typing import Callable, Dict, Optional

from keras_model_client.lib.ops import predict
from keras_model_client.lib.models import PredictionResult


OUTPUT_FORMATS = ('pretty', 'json')
DEFAULT_OUTPUT_FORMAT = 'pretty'
assert DEFAULT_OUTPUT_FORMAT in OUTPUT_FORMATS
DEFAULT_URL = 'https://adamant.tator.io:8082/predictor/'


def format_pretty(result: PredictionResult) -> str:
    lines = [f'Success: {result.success}']
    for prediction in result.predictions:
        bbox_str = '(' + ', '.join('{:.2f}'.format(v) for v in prediction.bbox) + ')'
        scores_str = 'score(s): ' + ' - '.join(
            '{:.2f}'.format(v) for v in prediction.scores
        )
        prediction_str = f'{prediction.category_id} ~ {bbox_str} ~ {scores_str}'
        lines.append(prediction_str)
    return '\n'.join(lines)


def format_json(result: PredictionResult) -> str:
    return result.to_json(indent=2)


def format_output(result: PredictionResult, format: str) -> Optional[str]:
    """
    Format the output to a string. Return None on invalid format.
    """
    HANDLERS: Dict[str, Callable[[PredictionResult], str]] = {
        'pretty': format_pretty,
        'json': format_json,
    }

    handler = HANDLERS.get(format, None)
    if not handler:
        print(f'Unimplemented output format: {format}', file=sys.stderr)
    else:
        return handler(result)


def output_result(result: PredictionResult, format: str):
    """
    Output a formatted result.
    """
    formatted_result = format_output(result, format)
    if formatted_result:
        print(formatted_result)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path, help='Path to image file')
    parser.add_argument('model_type', type=str, help='Model type to use in prediction')
    parser.add_argument(
        '-f',
        '--format',
        default=DEFAULT_OUTPUT_FORMAT,
        choices=OUTPUT_FORMATS,
        help=f'Output format, default: {DEFAULT_OUTPUT_FORMAT}',
    )
    parser.add_argument(
        '--url',
        type=str,
        default=DEFAULT_URL,
        help=f'Model server URL, default: {DEFAULT_URL}',
    )

    # Parse arguments
    args = parser.parse_args()
    image_path: Path = args.image

    # Ensure valid image path
    if not image_path.is_file():
        parser.error(f'Invalid image path: {image_path}')

    # Run the prediction and output
    try:
        result = predict(image_path, args.model_type, args.url)
        output_result(result, args.format)
    except Exception as e:
        print(f'Error while predicting {args.image}: {e}', file=sys.stderr)
