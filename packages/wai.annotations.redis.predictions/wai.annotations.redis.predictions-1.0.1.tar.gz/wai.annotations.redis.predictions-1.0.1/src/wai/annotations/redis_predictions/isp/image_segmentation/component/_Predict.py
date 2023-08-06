import io
import numpy as np

from PIL import Image

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from wai.annotations.domain.image.segmentation.util import UnlabelledInputMixin
from wai.annotations.redis_predictions.isp.base.component import BasePredict
from wai.common.cli.options import TypedOption

FORMAT_INDEXEDPNG = "indexedpng"
FORMAT_BLUECHANNEL = "bluechannel"
FORMATS = [
    FORMAT_INDEXEDPNG,
    FORMAT_BLUECHANNEL,
]


class Predict(
    BasePredict,
    UnlabelledInputMixin,
    ProcessorComponent[ImageSegmentationInstance, ImageSegmentationInstance]
):
    """
    Stream processor which makes image segmentation predictions via Redis backend.
    """

    image_format: str = TypedOption(
        "--image-format",
        type=str,
        default=FORMAT_INDEXEDPNG,
        help="the format of the image that comes back as prediction: %s" % ",".join(FORMATS)
    )

    def _fix_size(self, img, width, height):
        """
        Fixes the size of the received image, if necessary.

        :param img: the to resize
        :type img: Image
        :param width: the required width
        :type width: int
        :param height: the required height
        :type height: int
        :return: the (potentially) resized image
        :rtype: Image
        """
        if (img.width == width) and (img.height == height):
            return img
        else:
            return img.resize(width, height, Image.BILINEAR)

    def _process_predictions(self, element, data, then: ThenFunction[ImageSegmentationInstance], done: DoneFunction):
        """
        Processes the prediction data.

        :param element: the incoming image
        :param data: the data to process
        :param then: the function to call with the parsed prediction data
        :param done: if necessary to call
        :return:
        """

        annotations = ImageSegmentationAnnotation(labels=self.labels, size=element.annotations.size)

        w = element.data.width
        h = element.data.height

        # convert received image to indices
        if self.image_format == FORMAT_INDEXEDPNG:
            image = self._fix_size(Image.open(io.BytesIO(data)), w, h)
            new_indices = np.asarray(image).astype(np.uint16)
            new_indices.resize(element.annotations.indices.shape)
            annotations.indices = new_indices
        elif self.image_format == FORMAT_BLUECHANNEL:
            image = self._fix_size(Image.open(io.BytesIO(data)), w, h)
            new_indices = np.asarray(image).astype(np.uint16)
            new_indices.resize((*element.annotations.indices.shape, 3))
            new_indices = new_indices[:, :, 2]
            new_indices = new_indices.astype(np.uint16)
            annotations.indices = new_indices
        else:
            raise Exception("Unsupported image format: %s" % self.image_format)

        # update image
        result = element.__class__(element.data, annotations)
        then(result)
