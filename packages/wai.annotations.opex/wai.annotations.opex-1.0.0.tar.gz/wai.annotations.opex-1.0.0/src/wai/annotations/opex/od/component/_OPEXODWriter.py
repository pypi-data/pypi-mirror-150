import os
from datetime import datetime
from opex import ObjectPredictions

from wai.annotations.core.component.util import (
    SeparateFileWriter,
    SplitState,
    SplitSink,
    ExpectsDirectory,
    RequiresNoSplitFinalisation
)

from .._format import OPEXODFormat


class OPEXODWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SeparateFileWriter[OPEXODFormat],
    SplitSink[OPEXODFormat]
):
    """
    Writer of OPEX files.
    """

    # The path to write to for the split
    split_path: str = SplitState(
        lambda self: self.get_split_path(self.split_label, self.output)
    )

    def consume_element_for_split(
            self,
            element: OPEXODFormat
    ):
        # Unpack the instance
        image_info, opex_objects = element

        # Write the image
        self.write_data_file(image_info, self.split_path)

        # If the image is a negative, skip writing the annotations
        if len(opex_objects) == 0:
            return

        opex_ts = datetime.now().isoformat()
        opex_id = os.path.splitext(os.path.basename(image_info.filename))[0]
        objects = [x.prediction for x in opex_objects]
        opex_preds = ObjectPredictions(timestamp=opex_ts, id=opex_id, objects=objects)

        # Format the filename
        labels_filename = f"{os.path.splitext(image_info.filename)[0]}.json"

        # Write the annotations file
        opex_preds.save_json_to_file(os.path.join(self.split_path, labels_filename))

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output directory to write images and annotations to"
