from force_processor_bindings.workflows import ForceParameters, ForceProcessor  # noqa
from sen2like_processor_bindings.workflows import Sen2LikeParameters  # noqa
from sen2like_processor_bindings.workflows import Sen2LikeProcessor

from eodc import settings

Force = ForceProcessor(settings.FAAS_URL, namespace=settings.NAMESPACE)
Sen2Like = Sen2LikeProcessor(settings.FAAS_URL, namespace=settings.NAMESPACE)
