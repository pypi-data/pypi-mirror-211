from typing import Iterable, Tuple, Type

from tdm import TalismanDocument
from tdm.datamodel.directives import CreateConceptDirective
from tdm.datamodel.facts import ConceptFact

from tp_interfaces.abstract import ImmutableBaseModel
from tp_interfaces.knowledge_base.interfaces import KB
from tp_interfaces.knowledge_base.kb_schema import KBSchema

EMPTY_SCHEMA = KBSchema(tuple())


class DMBCommonnessStub(KB[ImmutableBaseModel]):
    def __init__(self, kb_schema: KBSchema = EMPTY_SCHEMA):
        self._kb_schema = kb_schema

    def __exit__(self, *exc):
        pass

    def refresh_schema(self):
        pass

    def bind_facts_and_load_docs(self, docs: Iterable[TalismanDocument]):
        pass

    def get_candidates(self, doc: TalismanDocument, config: ImmutableBaseModel
                       ) -> Tuple[Tuple[ConceptFact, ...], Tuple[CreateConceptDirective, ...]]:
        return tuple(), tuple()

    @property
    def config_type(self) -> Type[ImmutableBaseModel]:
        return ImmutableBaseModel

    @property
    def schema(self) -> KBSchema:
        return self._kb_schema

    @classmethod
    def from_config(cls, config: dict) -> 'DMBCommonnessStub':
        """Config example:
        {
            "schema": {
                ...`KBSchema` config...
            }
        }
        """
        return cls(kb_schema=KBSchema.from_config(config['schema']))
