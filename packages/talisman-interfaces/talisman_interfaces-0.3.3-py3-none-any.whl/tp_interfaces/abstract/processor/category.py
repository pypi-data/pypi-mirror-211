from collections import defaultdict
from typing import Callable, Dict, Generic, List, Optional, Sequence, Tuple, Type, TypeVar

from tdm import TalismanDocument

from tp_interfaces.abstract.model import AbstractCompositeModel
from tp_interfaces.abstract.schema import ImmutableBaseModel
from .processor import AbstractDocumentProcessor

_Config = TypeVar('_Config', bound=ImmutableBaseModel)
_Category = TypeVar('_Category')


class AbstractCategoryAwareDocumentProcessor(
    AbstractCompositeModel[AbstractDocumentProcessor[_Config]],
    AbstractDocumentProcessor[_Config], Generic[_Config, _Category]
):
    def __init__(self,
                 category2processor: Dict[_Category, AbstractDocumentProcessor[_Config]],
                 categorizer: Callable[[TalismanDocument], _Category],
                 default_processor: Optional[AbstractDocumentProcessor[_Config]] = None
                 ):
        self._category2processor = dict(category2processor)
        super().__init__(self._category2processor.values())
        self._models: Tuple[AbstractDocumentProcessor[_Config], ...]
        self._categorizer = categorizer
        self._default = default_processor

    def process_doc(self, document: TalismanDocument, config: _Config) -> TalismanDocument:
        return self.process_docs([document], config)[0]

    def process_docs(self, documents: Sequence[TalismanDocument], config: _Config) \
            -> Tuple[TalismanDocument, ...]:
        category2doc = defaultdict(dict)
        processed_docs: List[Optional[TalismanDocument]] = [None] * len(documents)

        for i, doc in enumerate(documents):
            category = self._categorizer(doc)
            category2doc[category].update({i: doc})

        for category, docs in category2doc.items():
            processor = self._category2processor.get(category, self._default)
            if processor is None:
                raise ValueError(f"No processor registered for {category} (available categories: {list(self._category2processor)})")
            docs_ = processor.process_docs(tuple(docs.values()), config)
            for id_, doc in zip(docs, docs_):
                processed_docs[id_] = doc

        return tuple(processed_docs)

    @property
    def config_type(self) -> Type[_Config]:
        return self._models[0].config_type
