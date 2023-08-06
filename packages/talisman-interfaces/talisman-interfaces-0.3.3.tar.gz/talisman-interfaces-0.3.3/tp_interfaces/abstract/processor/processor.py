from abc import ABCMeta, abstractmethod
from functools import partial
from itertools import chain
from typing import Generic, Iterator, Sequence, Tuple, Type, TypeVar

from more_itertools import ichunked
from tdm import TalismanDocument

from tp_interfaces.abstract.model import AbstractModel
from tp_interfaces.abstract.schema import ImmutableBaseModel
from tp_interfaces.logging.context import with_log_extras

_Config = TypeVar('_Config', bound=ImmutableBaseModel)


class AbstractDocumentProcessor(AbstractModel, Generic[_Config], metaclass=ABCMeta):

    @abstractmethod
    def process_doc(self, document: TalismanDocument, config: _Config) -> TalismanDocument:
        pass

    def process_docs(self, documents: Sequence[TalismanDocument], config: _Config) \
            -> Tuple[TalismanDocument, ...]:
        log_extras = with_log_extras(doc_id=lambda kwargs: kwargs['document'].id)
        return tuple(map(partial(log_extras(self.process_doc), config=config), documents))

    def process_stream(self, documents: Iterator[TalismanDocument], config: _Config, batch_size: int) \
            -> Iterator[TalismanDocument]:
        return chain.from_iterable(map(partial(self.process_docs, config=config), map(tuple, ichunked(documents, batch_size))))

    @property
    @abstractmethod
    def config_type(self) -> Type[_Config]:
        pass
