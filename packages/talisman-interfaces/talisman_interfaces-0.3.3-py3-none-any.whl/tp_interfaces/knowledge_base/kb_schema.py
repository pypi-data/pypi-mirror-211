from abc import ABCMeta
from typing import Any, Dict, Iterable, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, Extra, validator
from tdm.abstract.datamodel import AbstractFact, AbstractValue
from tdm.datamodel.facts import AtomValueFact, CompositeValueFact, ConceptFact, PropertyFact, RelationFact, \
    RelationPropertyFact, SlotFact

from tp_interfaces.abstract import ImmutableBaseModel

_Label = TypeVar("_Label", bound=Any)


class AbstractSchemaType(ImmutableBaseModel, metaclass=ABCMeta):
    id: str
    name: str

    class Config:
        extra = Extra.ignore


class NERCRegexp(ImmutableBaseModel):
    regexp: str
    context_regexp: Optional[str] = None
    auto_create: bool = False

    @validator('auto_create', pre=True)
    def non_null(cls, v):  # noqa: N805
        return v or False


class SchemaConceptType(AbstractSchemaType):
    regexp: Tuple[NERCRegexp, ...] = tuple()
    black_regexp: Tuple[NERCRegexp, ...] = tuple()
    pretrained_nercmodels: Tuple[str, ...] = tuple()
    dictionary: Tuple[str, ...] = tuple()
    black_list: Tuple[str, ...] = tuple()


class SchemaValueType(SchemaConceptType):
    value_type: Type[AbstractValue]
    value_restriction: Optional[Tuple[str, ...]]


class RelExtModel(ImmutableBaseModel):
    source_annotation: Optional[str]
    target_annotation: Optional[str]
    relation_type: Optional[str]
    invert_direction: Optional[bool]


class SchemaRelationType(AbstractSchemaType):
    from_id: str
    to_id: str
    pretrained_relext_models: Tuple[RelExtModel, ...] = tuple()
    is_directed: bool = True


_SchemaType = TypeVar('_SchemaType', bound=AbstractSchemaType)
FACT_TYPE_SCHEMAS = {
    ConceptFact: SchemaConceptType,
    AtomValueFact: SchemaValueType,
    CompositeValueFact: SchemaValueType,
    SlotFact: SchemaRelationType,
    PropertyFact: SchemaRelationType,
    RelationFact: SchemaRelationType,
    RelationPropertyFact: SchemaRelationType
}


class KBSchema:
    def __init__(self, types: Iterable[_SchemaType]):
        self._id2type: Dict[str, _SchemaType] = {}

        for type_ in types:
            self._id2type[type_.id] = type_

    def get_type(self, id_: str) -> Optional[_SchemaType]:
        return self._id2type.get(id_, None)

    @classmethod
    def from_config(cls, config: dict) -> 'KBSchema':
        """Config example:
        {
            "types": [
                ... List of serialized `AnySchemaType` objects ...
            ]
        }
        """

        class SoftSchemaType(BaseModel):
            fact_type: Type[AbstractFact]  # FIXME: looks like not working solution (tests are required)

        def convert_to_schema_type(schema_attributes: dict) -> _SchemaType:
            soft_type = SoftSchemaType.parse_obj(schema_attributes)
            hard_type = FACT_TYPE_SCHEMAS[soft_type.fact_type]
            return hard_type.parse_obj(schema_attributes)

        return cls(map(convert_to_schema_type, config['types']))
