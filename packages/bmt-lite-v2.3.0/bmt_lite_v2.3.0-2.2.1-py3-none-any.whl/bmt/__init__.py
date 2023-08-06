"""BMT basics."""
from typing import Dict, List, Optional

from .data import (
    all_classes, all_elements, all_slots, all_types,
    alias_ancestors, basic_ancestors, mixin_ancestors, alias_mixin_ancestors,
    alias_descendants, basic_descendants, mixin_descendants, alias_mixin_descendants,
    alias_children, basic_children, mixin_children, alias_mixin_children,
    parent, element,
)
from .util import with_formatting


class Toolkit():
    """Biolink model toolkit - lite!"""

    def __init__(self, schema=None):
        """Initialize."""
        if schema is not None:
            raise ValueError("bmt-lite does not support the `schema` argument. The biolink model version is dictated by the library flavor you installed.")

    def get_all_classes(self) -> List[str]:
        """Get all classes."""
        return all_classes

    def get_all_slots(self) -> List[str]:
        """Get all slots."""
        return all_slots

    def get_all_types(self) -> List[str]:
        """Get all types."""
        return all_types

    def get_all_elements(self) -> List[str]:
        """Get all elements."""
        return all_elements

    @with_formatting()
    def get_ancestors(
        self,
        name: str,
        reflexive: bool = True,
        mixin: bool = True,
        alias: bool = False,
    ) -> List[str]:
        """Get ancestors."""
        _ancestors = basic_ancestors.get(name, [])
        if mixin:
            _ancestors += mixin_ancestors.get(name, [])
        if alias:
            _ancestors += alias_ancestors.get(name, [])
        if mixin and alias:
            _ancestors += alias_mixin_ancestors.get(name, [])
        if reflexive:
            return _ancestors + [name]
        else:
            return _ancestors

    @with_formatting()
    def get_descendants(
        self,
        name: str,
        reflexive: bool = True,
        mixin: bool = True,
        alias: bool = False,
    ) -> List[str]:
        """Get descendants."""
        _descendants = basic_descendants.get(name, [])
        if mixin:
            _descendants += mixin_descendants.get(name, [])
        if alias:
            _descendants += alias_descendants.get(name, [])
        if mixin and alias:
            _descendants += alias_mixin_descendants.get(name, [])
        if reflexive:
            return _descendants + [name]
        else:
            return _descendants

    @with_formatting()
    def get_children(
        self,
        name: str,
        mixin: bool = True,
        alias: bool = False,
    ) -> List[str]:
        """Get children."""
        _children = basic_children.get(name, [])
        if mixin:
            _children += mixin_children.get(name, [])
        if alias:
            _children += alias_children.get(name, [])
        if mixin and alias:
            _children += alias_mixin_children.get(name, [])
        return _children

    @with_formatting()
    def get_parent(
        self,
        name: str,
    ) -> Optional[str]:
        """Get parent."""
        return parent.get(name, None)

    @with_formatting()
    def get_element(
        self,
        name: str,
    ) -> Optional["Element"]:
        """Get element."""
        if name in all_classes:
            return ClassDefinition(name, **element.get(name, dict()))
        elif name in all_slots:
            return SlotDefinition(name, **element.get(name, dict()))
        return None


class AttrDict(dict):
    """https://stackoverflow.com/a/14620633"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class Element(AttrDict):
    """Biolink model element."""

    def __init__(self, name: str):
        """Initialize."""
        super().__init__()
        self.name: str = name


class SlotDefinition(Element):
    """Slot definition."""

    def __init__(
        self,
        name: str,
        symmetric: bool = False,
        inverse: Optional[str] = None,
        annotations: Dict[str, bool] = dict(),
        slot_uri: Optional[str] = None,
        range: Optional[str] = None,
        **kwargs,
    ):
        """Initialize."""
        super().__init__(name)
        self.symmetric: bool = symmetric
        self.inverse: Optional[str] = inverse
        self.annotations: Dict[str, bool] = annotations
        self.slot_uri: Optional[str] = slot_uri
        self.range: Optional[str] = range


class ClassDefinition(Element):
    """Class definition."""

    def __init__(
        self,
        name: str,
        id_prefixes: List[str],
        mixins: List[str],
    ):
        """Initialize."""
        super().__init__(name)
        self.id_prefixes: List[str] = id_prefixes
        self.mixins: List[str] = mixins
