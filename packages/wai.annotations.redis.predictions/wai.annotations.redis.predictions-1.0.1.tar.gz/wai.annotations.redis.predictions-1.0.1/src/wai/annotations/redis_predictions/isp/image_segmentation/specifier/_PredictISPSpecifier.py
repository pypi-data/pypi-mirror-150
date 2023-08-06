from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class PredictISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the image segmentation predict ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Makes image segmentation predictions via Redis backend, passing in an image and receiving an image with predicted segmentations."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageSegmentationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Predict only handles the following domains: "
                f"{ImageSegmentationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.redis_predictions.isp.image_segmentation.component import Predict
        return Predict,
