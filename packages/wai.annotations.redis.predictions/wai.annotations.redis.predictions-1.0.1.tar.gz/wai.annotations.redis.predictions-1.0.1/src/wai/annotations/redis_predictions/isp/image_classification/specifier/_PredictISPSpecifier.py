from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class PredictISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the annotation_overlay image ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Makes image classification predictions via Redis backend, passing in an image and receiving JSON predictions back (at least one of 'label: probability').\n" \
               + "Predictions example:\n" \
               + "{\"dog\": 0.9, \"cat\": 0.1}"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Predict only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.redis_predictions.isp.image_classification.component import Predict
        return Predict,
