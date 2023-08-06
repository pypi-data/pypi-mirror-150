"""
API models.
"""

from typing import List
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Prediction:
    category_id: str
    scores: List[float]
    bbox: List[float]


@dataclass_json
@dataclass
class PredictionResult:
    success: bool
    predictions: List[Prediction]
