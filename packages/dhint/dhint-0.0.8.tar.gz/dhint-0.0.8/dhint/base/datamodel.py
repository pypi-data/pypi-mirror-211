from __future__ import annotations

__all__ = ['BaseDataclass']

from abc import ABCMeta
from typing import get_type_hints
from dataclasses import dataclass
from ._meta import *

@dataclass
class BaseDataclass(MetaField, MetaName, MetaDescriptor, metaclass=ABCMeta):

    @property
    def repr_string(self):
        items = (f"{d.public_name}={d.get(self)!r}" for d in self.repr_descriptors())
        return "{}({})".format(type(self).__name__, ", ".join(items))
    
    @classmethod
    def class_setup(cls):
        pass
    
    @classmethod
    def type_hints(cls):
        return get_type_hints(cls)
    

    

