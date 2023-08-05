import os

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.util import get_associated_image
from opex import ObjectPredictions

from .._format import OPEXODFormat, OPEXObject


class OPEXODReader(AnnotationFileProcessor[OPEXODFormat]):
    """
    Reader of OPEX object-detection files.
    """

    def read_annotation_file(
            self,
            filename: str,
            then: ThenFunction[OPEXODFormat]
    ):

        # Split the filename into path, basename, ext
        path, basename = os.path.split(filename)
        basename, extension = os.path.splitext(basename)

        # Find the image
        image_filename = get_associated_image(os.path.join(path, basename))

        # Read the OPEX annotations
        opex_preds = ObjectPredictions.load_json_from_file(filename)
        objects = []
        for obj in opex_preds.objects:
            objects.append(OPEXObject(prediction=obj, label=obj.label))

        # Read the image
        image = Image.from_file(image_filename)

        then((image, tuple(objects)))

    def read_negative_file(
            self,
            filename: str,
            then: ThenFunction[OPEXODFormat]
    ):
        image_info = Image.from_file(filename)

        then((image_info, None))
