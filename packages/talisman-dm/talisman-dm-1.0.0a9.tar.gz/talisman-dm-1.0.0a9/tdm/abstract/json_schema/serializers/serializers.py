from typing import Any, Callable

from tdm.abstract.datamodel import AbstractDomainType, AbstractFact, AbstractMarkup, AbstractNode, AbstractNodeMention, AbstractValue, \
    BaseNodeMetadata
from .dataclass import DataclassSerializer
from .domain import DomainTypeSerializer
from .identifiable import IdSerializer
from .markup import MarkupSerializer
from .mention import NodeMentionSerializer
from .metadata import NodeMetadataSerializer
from .type_ import TypeSerializer
from .value import ValueSerializer


def _issubclass(t: type) -> Callable[[Any], bool]:
    def criteria(obj: Any) -> bool:
        return issubclass(obj, t)

    return criteria


def _is(t: object) -> Callable[[Any], bool]:
    def criteria(obj: Any) -> bool:
        return obj is t

    return criteria


def _hasattr(attr: str) -> Callable[[Any], bool]:
    def criteria(obj: Any) -> bool:
        return hasattr(obj, attr)

    return criteria


def build_serializers():
    result = {
        _issubclass(AbstractNode): IdSerializer(AbstractNode),
        _issubclass(AbstractFact): IdSerializer(AbstractFact),
        _issubclass(AbstractNodeMention): NodeMentionSerializer(),
        _issubclass(BaseNodeMetadata): NodeMetadataSerializer(),
        _issubclass(AbstractValue): ValueSerializer(),
        _issubclass(AbstractMarkup): MarkupSerializer(),
        _issubclass(AbstractDomainType): DomainTypeSerializer(),
        _hasattr('__dataclass_fields__'): DataclassSerializer(),
        _is(type): TypeSerializer()
    }
    # other serializers could be added here
    return result
