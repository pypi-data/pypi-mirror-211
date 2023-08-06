from force_processor_bindings.model import ForceParameters, ForceResMergeOptions  # noqa
from force_processor_bindings.workflows import ForceProcessor
from sen2like_processor_bindings.model import BoundingBox as Sen2LikeBoundingBox  # noqa
from sen2like_processor_bindings.model import (  # noqa
    Sen2LikeParameters,
    sen2like_options,
)
from sen2like_processor_bindings.workflows import Sen2LikeProcessor

from eodc import settings


class Force(ForceProcessor):
    @classmethod
    def get_instance(cls):
        return cls(endpoint_url=settings.FAAS_URL, namespace=settings.NAMESPACE)


class Sen2Like(Sen2LikeProcessor):
    @classmethod
    def get_instance(cls):
        return cls(endpoint_url=settings.FAAS_URL, namespace=settings.NAMESPACE)
