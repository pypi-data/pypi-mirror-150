from functools import partial
from typing import Dict, Optional

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import OutputElementType, ThenFunction, DoneFunction
from wai.annotations.core.stream.util import ProcessState
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.object_detection.util import get_object_label
from wai.common.adams.imaging.locateobjects import LocatedObject
from wai.common.cli.options import TypedOption
from opex import ObjectPrediction, BBox, Polygon

from .._format import OPEXODFormat, OPEXObject


class ToOPEXOD(
    ProcessorComponent[ImageObjectDetectionInstance, OPEXODFormat]
):
    """
    Converter from internal format to OPEX annotations.
    """
    # Path to the labels file to write
    labels_file: Optional[str] = TypedOption(
        "-l", "--labels",
        type=str,
        metavar="PATH",
        help="Path to the labels file to write"
    )

    # Path to the labels CSV file to write
    labels_csv_file: Optional[str] = TypedOption(
        "-c", "--labels-csv",
        type=str,
        metavar="PATH",
        help="Path to the labels CSV file to write"
    )

    # Label-index mapping accumulator
    labels: Dict[str, int] = ProcessState(lambda self: {})

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[OPEXODFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        if located_objects is None or len(located_objects) == 0:
            return then((image_info, tuple()))

        to_opex_object = partial(self.to_opex_object)
        opex_objects = tuple(map(to_opex_object, located_objects))

        then((image_info, opex_objects))

    def finish(self, then: ThenFunction[OutputElementType], done: DoneFunction):
        # Write the labels file
        if self.labels_file is not None:
            with open(self.labels_file, "w") as labels_file:
                labels_file.write(",".join(self.labels.keys()))

        # Write the labels CSV file
        if self.labels_csv_file is not None:
            with open(self.labels_csv_file, "w") as labels_csv_file:
                labels_csv_file.write("Index,Label")
                for label, index in self.labels.items():
                    labels_csv_file.write(f"\n{index},{label}")

        done()

    def to_opex_object(self, located_object: LocatedObject) -> OPEXObject:
        """
        Converts a single located object into a OPEX object.

        :param located_object:
                    The located object to convert.
        :return:
                    The OPEX object.
        """
        # Update the label mapping
        label = get_object_label(located_object)
        if label not in self.labels:
            self.labels[label] = len(self.labels)

        bbox = BBox(
            left=located_object.x,
            top=located_object.y,
            right=located_object.x + located_object.width - 1,
            bottom=located_object.y + located_object.height - 1)
        points = []
        if located_object.has_polygon():
            xs = located_object.get_polygon_x()
            ys = located_object.get_polygon_y()
            for x, y in zip(xs, ys):
                points.append([x, y])
        else:
            points.append([bbox.left, bbox.top])
            points.append([bbox.right, bbox.top])
            points.append([bbox.right, bbox.bottom])
            points.append([bbox.left, bbox.bottom])

        polygon = Polygon(points=points)
        opex_pred = ObjectPrediction(label=label, bbox=bbox, polygon=polygon)

        return OPEXObject(prediction=opex_pred, label=label)
