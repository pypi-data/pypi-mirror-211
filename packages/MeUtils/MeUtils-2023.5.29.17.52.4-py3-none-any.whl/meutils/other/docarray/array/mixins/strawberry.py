from typing import TYPE_CHECKING, Type, List

if TYPE_CHECKING:  # pragma: no cover
    from meutils.docarray_.typing import T
    from meutils.docarray_.document.strawberry_type import StrawberryDocument


class StrawberryMixin:
    def to_strawberry_type(self) -> List['StrawberryDocument']:
        """Convert a DocumentArray object into a Pydantic model."""
        return [d.to_strawberry_type() for d in self]

    @classmethod
    def from_strawberry_type(cls: Type['T'], model: List['StrawberryDocument']) -> 'T':
        """Convert a list of Strawberry into DocumentArray

        :param model: the list of strawberry type objects that represents a DocumentArray
        :return: a DocumentArray
        """
        from meutils.docarray_ import Document

        return cls(Document.from_strawberry_type(m) for m in model)
