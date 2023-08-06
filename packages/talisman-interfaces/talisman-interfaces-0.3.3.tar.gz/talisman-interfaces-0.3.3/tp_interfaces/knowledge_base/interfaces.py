from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import Generic, Tuple, Type, TypeVar

from tdm import TalismanDocument
from tdm.datamodel.directives import CreateConceptDirective
from tdm.datamodel.facts import ConceptFact

from tp_interfaces.abstract import ImmutableBaseModel
from tp_interfaces.knowledge_base.kb_schema import KBSchema

_DMBConfigInterface = TypeVar('_DMBConfigInterface', bound=ImmutableBaseModel)


class LoaderKB(AbstractContextManager, metaclass=ABCMeta):
    @abstractmethod
    def bind_facts_and_load_docs(self, docs: Tuple[TalismanDocument, ...]):
        pass

    @property
    @abstractmethod
    def schema(self) -> KBSchema:
        pass

    @abstractmethod
    def refresh_schema(self):
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> 'LoaderKB':
        pass


class DisambiguationKB(AbstractContextManager, Generic[_DMBConfigInterface], metaclass=ABCMeta):
    @abstractmethod
    def get_candidates(self, doc: TalismanDocument, config: _DMBConfigInterface
                       ) -> Tuple[Tuple[ConceptFact, ...], Tuple[CreateConceptDirective, ...]]:
        pass

    @property
    @abstractmethod
    def config_type(self) -> Type[_DMBConfigInterface]:
        pass

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> 'DisambiguationKB':
        pass


class KB(LoaderKB, DisambiguationKB, Generic[_DMBConfigInterface], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> 'KB':
        pass
