"""Biolink model data."""
import json
from typing import Dict, List, Optional

import importlib.resources as pkg_resources

from . import _data

with pkg_resources.open_text(_data, "all_classes.json") as stream:
    all_classes: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_elements.json") as stream:
    all_elements: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_slots.json") as stream:
    all_slots: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "all_types.json") as stream:
    all_types: List[str] = json.load(stream)
with pkg_resources.open_text(_data, "alias_ancestors.json") as stream:
    alias_ancestors: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "basic_ancestors.json") as stream:
    basic_ancestors: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "mixin_ancestors.json") as stream:
    mixin_ancestors: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "alias_mixin_ancestors.json") as stream:
    alias_mixin_ancestors: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "alias_descendants.json") as stream:
    alias_descendants: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "basic_descendants.json") as stream:
    basic_descendants: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "mixin_descendants.json") as stream:
    mixin_descendants: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "alias_mixin_descendants.json") as stream:
    alias_mixin_descendants: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "alias_children.json") as stream:
    alias_children: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "basic_children.json") as stream:
    basic_children: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "mixin_children.json") as stream:
    mixin_children: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "alias_mixin_children.json") as stream:
    alias_mixin_children: Dict[str, List[str]] = json.load(stream)
with pkg_resources.open_text(_data, "parent.json") as stream:
    parent: Dict[str, Optional[str]] = json.load(stream)
with pkg_resources.open_text(_data, "element.json") as stream:
    element: Dict[str, Dict] = json.load(stream)
