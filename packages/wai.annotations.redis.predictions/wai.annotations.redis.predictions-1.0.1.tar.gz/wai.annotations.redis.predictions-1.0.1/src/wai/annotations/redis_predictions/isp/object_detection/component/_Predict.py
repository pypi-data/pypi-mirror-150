from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.redis_predictions.isp.base.component import BasePredict
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption
from wai.common.geometry import Polygon, Point
from opex import ObjectPredictions


class Predict(
    BasePredict,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Stream processor which makes object detection predictions via Redis backend.
    """

    key_label: str = TypedOption(
        "--key-label",
        type=str,
        default="type",
        help="the meta-data key in the annotations to use for storing the label."
    )

    key_score: str = TypedOption(
        "--key-score",
        type=str,
        default="score",
        help="the meta-data key in the annotations to use for storing the prediction score."
    )

    def _process_predictions(self, element, data, then: ThenFunction[ImageObjectDetectionInstance], done: DoneFunction):
        """
        Processes the prediction data.

        :param element: the incoming image
        :param data: the data to process
        :param then: the function to call with the parsed prediction data
        :param done: if necessary to call
        :return:
        """
        # convert to wai.annotations annotations
        oobjects = ObjectPredictions.from_json_string(data)
        lobjects = []
        for oobject in oobjects.objects:
            # bbox
            obbox = oobject.bbox
            x = obbox.left
            y = obbox.top
            w = obbox.right - obbox.left + 1
            h = obbox.bottom - obbox.top + 1

            # polygon
            opoly = oobject.polygon
            lpoints = []
            for opoint in opoly.points:
                lpoints.append(Point(x=opoint[0], y=opoint[1]))
            lpoly = Polygon(*lpoints)

            # metadata
            metadata = dict()
            if hasattr(oobject, "score"):
                metadata[self.key_score] = oobject.score
            metadata[self.key_label] = oobject.label

            # add object
            located_object = LocatedObject(x, y, w, h, **metadata)
            located_object.set_polygon(lpoly)
            lobjects.append(located_object)

        annotations = LocatedObjects(lobjects)

        # update image
        result = element.__class__(element.data, annotations)
        then(result)
