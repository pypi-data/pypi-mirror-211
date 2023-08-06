from __future__ import annotations

__all__ = ['MetaDescriptor', 'MetaName', 'MetaField', 'isinitvarfield', 'isclassvarfield', 'isinstancefield']

from abc import ABC
from typing_extensions import Self
from typing import Optional, Any, ClassVar
from collections import ChainMap
from functools import partialmethod, cache
from dataclasses import dataclass, Field, fields, asdict, astuple
from dhint.functions import *
from .descriptor import *


def isinstancefield(obj: Any) -> bool:
    return isinstance(obj, Field)


def isclassvarfield(field: Field) -> bool:
    return isinstancefield(field) and str(field.type).__contains__('ClassVar')


def isinitvarfield(field: Field) -> bool:
    return isinstancefield(field) and str(field.type).__contains__('InitVar')


class MetaDescriptor(ABC):
    DESCRIPTORS: ClassVar[dict[str, BaseDescriptor]] = None
    
    @classmethod
    def bases(cls):
        return tuple([item for item in cls.mro() if issubclass(item, cls.base_subclass()) if
                      not item is cls.base_subclass()])
    
    @classmethod
    def base_subclass(cls):
        return cls
    
    @classmethod
    def descriptors(cls) -> dict[str, BaseDescriptor]:
        if not cls.DESCRIPTORS:
            mapping = ChainMap(*[vars(item) for item in cls.bases()])
            cls.DESCRIPTORS = {k: value for k, value in mapping.items() if isinstance(value, BaseDescriptor)}
        return cls.DESCRIPTORS
    
    @classmethod
    def descriptor(cls, name: str) -> BaseDescriptor:
        return cls.descriptors().get(name, None)
    
    @classmethod
    @cache
    def filter_descriptors(cls, name: str, value: Any) -> tuple[BaseDescriptor]:
        return tuple([d for d in cls.descriptors_values() if getattr(d, name, None) == value])
    
    datalist_descriptors = partialmethod(filter_descriptors, 'datalist', True)
    hash_descriptors = partialmethod(filter_descriptors, 'hash', True)
    frozen_descriptors = partialmethod(filter_descriptors, 'frozen', True)
    required_descriptors = partialmethod(filter_descriptors, 'is_required', True)
    private_descriptors = partialmethod(filter_descriptors, 'private', True)
    repr_descriptors = partialmethod(filter_descriptors, 'repr', True)
    db_descriptors = partialmethod(filter_descriptors, 'db', True)
    no_db_descriptors = partialmethod(filter_descriptors, 'db', False)
    no_form_descriptors = partialmethod(filter_descriptors, 'no_form', True)
    input_descriptors = partialmethod(filter_descriptors, 'is_input', True)
    textarea_descriptors = partialmethod(filter_descriptors, 'is_textarea', True)
    select_descriptors = partialmethod(filter_descriptors, 'is_select', True)
    htmx_descriptors = partialmethod(filter_descriptors, 'htmx', True)
    search_descriptors = partialmethod(filter_descriptors, 'search', True)
    compare_descriptors = partialmethod(filter_descriptors, 'compare', True)
    range_descriptors = partialmethod(filter_descriptors, 'is_range', True)
    hidden_descriptors = partialmethod(filter_descriptors, 'is_hidden', True)
    checkbox_descriptors = partialmethod(filter_descriptors, 'is_checkbox', True)
    
    @classmethod
    def descriptors_values(cls) -> tuple[BaseDescriptor]:
        return tuple(cls.descriptors().values())
    
    @classmethod
    def descriptors_keys(cls) -> tuple[str]:
        return tuple(cls.descriptors().keys())
    
    @classmethod
    def descriptor_by_type(cls, dt: type[BaseDescriptor]):
        return tuple([d for d in cls.descriptors_values() if isinstance(d, dt)])
    
    @property
    def search_getter(self):
        search = self.search_descriptors()
        if len(search) > 0:
            return normalize_lower(' '.join([str(d.get(self)) for d in search]))
        return normalize_lower(str(self))


class MetaName(ABC):
    PLURAL: ClassVar[Optional[str]] = None
    SINGULAR: ClassVar[Optional[str]] = None
    
    @classmethod
    def class_name(cls):
        return cls.__name__
    
    @classmethod
    def singular(cls) -> str:
        return cls.SINGULAR or cls.class_name()
    
    @classmethod
    def plural(cls) -> str:
        return cls.PLURAL or f'{cls.singular()}s'


@dataclass
class MetaField(ABC):
    INITVARS_NAMES: ClassVar[tuple[str]] = None
    INITFIELDS_NAMES: ClassVar[tuple[str]] = None
    FIELDS_NAMES: ClassVar[tuple[str]] = None
    FIELDS: ClassVar[dict[str, Field]] = None
    
    @classmethod
    def fields(cls) -> dict[str, Field]:
        if not cls.FIELDS:
            cls.FIELDS = {item.name: item for item in fields(cls)}
        return cls.FIELDS
    
    @classmethod
    def field(cls, name: str) -> Field:
        return cls.fields().get(name, None)
    
    @classmethod
    def fields_names(cls) -> tuple[str]:
        if not cls.FIELDS_NAMES:
            cls.FIELDS_NAMES = tuple(cls.fields().keys())
        return cls.FIELDS_NAMES
    
    @classmethod
    def filter_fields(cls, data: dict) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls.fields_names()}
    
    @classmethod
    def all_fields(cls) -> dict[str, Field]:
        return vars(cls)['__dataclass_fields__']
    
    @classmethod
    def init_fields(cls) -> dict[str, Field]:
        return {k: value for k, value in cls.all_fields().items() if not isclassvarfield(value)}
    
    @classmethod
    def initvar_fields(cls) -> dict[str, Field]:
        return {k: v for k, v in cls.all_fields().items() if isinitvarfield(v)}
    
    @classmethod
    def classvar_fields(cls) -> dict[str, Field]:
        return {k: v for k, v in cls.all_fields().items() if isclassvarfield(v)}
    
    def asdict(self) -> dict[str, Any]:
        return asdict(self)
    
    def astuple(self) -> tuple:
        return astuple(self)
    
    @classmethod
    def filter_initfields(cls, data: dict) -> dict[str, Any]:
        return {k: v for k, v in data.items() if k in cls.initfields_names()}
    
    @classmethod
    def initfields_names(cls) -> tuple[str]:
        if not cls.INITFIELDS_NAMES:
            cls.INITFIELDS_NAMES = tuple([k for k in cls.init_fields()])
        return cls.INITFIELDS_NAMES
    
    @classmethod
    def create(cls, *args, **kwargs) -> Optional[Self]:
        return cls(*args, **cls.filter_initfields(kwargs))
    
    @classmethod
    def initvars_names(cls) -> tuple[str]:
        if not cls.INITVARS_NAMES:
            cls.INITVARS_NAMES = tuple(cls.initvar_fields().keys())
        return cls.INITVARS_NAMES



