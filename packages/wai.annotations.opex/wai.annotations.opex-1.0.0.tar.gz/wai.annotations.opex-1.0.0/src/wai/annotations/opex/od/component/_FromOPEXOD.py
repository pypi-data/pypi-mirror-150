from functools import partial

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.object_detection.util import set_object_label
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point

from .._format import OPEXODFormat, OPEXObject


class FromOPEXOD(
    RequiresNoFinalisation,
    ProcessorComponent[OPEXODFormat, ImageObjectDetectionInstance]
):
    """
    Converter from OPEX annotations to internal format.
    """

    def process_element(
            self,
            element: OPEXODFormat,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        # Unpack the external format
        image_info, opex_objects = element

        # Convert OPEX objects to located objects
        located_objects = None
        if len(opex_objects) > 0:
            to_located_object = partial(self.to_located_object)
            located_objects = LocatedObjects(map(to_located_object, opex_objects))

        then(
            ImageObjectDetectionInstance(
                image_info,
                located_objects
            )
        )

    def to_located_object(self, object: OPEXObject) -> LocatedObject:
        """
        Converts the OPEX object to a located object.

        :param object:
                    The OPEX object.
        :return:
                    The located object.
        """
        # Get the object label (just uses the class index if no mapping is provided)
        label: str = object.label

        bbox = object.prediction.bbox
        poly = object.prediction.polygon
        points = []
        for x, y in poly.points:
            points.append(Point(x=x, y=y))

        # Create the located object
        located_object = LocatedObject(bbox.left, bbox.top, bbox.right - bbox.left + 1, bbox.bottom - bbox.top + 1)
        located_object.set_polygon(Polygon(*points))
        set_object_label(located_object, label)

        return located_object
