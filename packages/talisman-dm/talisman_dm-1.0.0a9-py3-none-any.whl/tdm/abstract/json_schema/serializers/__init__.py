__all__ = [
    'AbstractElementModel', 'AbstractElementSerializer', 'AbstractModelSerializer',
    'IdSerializer',
    'NodeMentionSerializer',
    'NodeMetadataSerializer',
    'BaseSerializers'
]

from typing import Any, Callable, Mapping

from immutabledict import immutabledict

from .abstract import AbstractElementModel, AbstractElementSerializer, AbstractModelSerializer
from .identifiable import IdSerializer
from .mention import NodeMentionSerializer
from .metadata import NodeMetadataSerializer
from .serializers import build_serializers

BaseSerializers: Mapping[Callable[[Any], bool], AbstractElementSerializer] = immutabledict(build_serializers())
