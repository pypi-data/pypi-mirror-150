from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class PredictISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the object detection predict ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Makes object detection predictions via Redis backend, passing in an image and receiving OPEX predictions back:\n" \
               + "https://github.com/WaikatoLink2020/objdet-predictions-exchange-format"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Predict only handles the following domains: "
                f"{ImageObjectDetectionDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.redis_predictions.isp.object_detection.component import Predict
        return Predict,
