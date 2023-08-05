from dataclasses import dataclass
from typing import Tuple

from wai.annotations.domain.image import Image
from opex import ObjectPrediction


@dataclass
class OPEXObject:
    """
    Internal representation of an OPEX annotation.
    """
    prediction: ObjectPrediction
    label: str

    @classmethod
    def from_string(cls, string: str):
        return ObjectPrediction.from_json_string(string)

    def __str__(self):
        return self.prediction.to_json_string()


OPEXODFormat = Tuple[Image, Tuple[OPEXObject]]
