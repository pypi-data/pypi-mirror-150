import json

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image.classification import ImageClassificationInstance
from wai.annotations.domain.classification import Classification
from wai.annotations.redis_predictions.isp.base.component import BasePredict


class Predict(
    BasePredict,
    ProcessorComponent[ImageClassificationInstance, ImageClassificationInstance]
):
    """
    Stream processor which makes image classification predictions via Redis backend.
    """

    def _process_predictions(self, element, data, then: ThenFunction[ImageClassificationInstance], done: DoneFunction):
        """
        Processes the prediction data.

        :param element: the incoming image
        :param data: the data to process
        :param then: the function to call with the parsed prediction data
        :param done: if necessary to call
        :return:
        """
        # convert to wai.annotations annotations
        preds = json.loads(data)
        max_key = None
        max_value = 0.0
        for k in preds:
            if preds[k] > max_value:
                max_key = k
                max_value = preds[k]

        annotations = Classification(label=max_key)

        # update image
        result = element.__class__(element.data, annotations)
        then(result)
