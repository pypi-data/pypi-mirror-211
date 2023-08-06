from __future__ import annotations

__all__ = ['BaseDetaModel']


from typing import Optional, ClassVar
from dataclasses import dataclass
from dhint.functions import *
from .datamodel import *

@dataclass
class BaseDetaModel(BaseDataclass):
    TABLE: ClassVar[Optional[str]] = None
    ITEM_NAME: ClassVar[Optional[str]] = None
    
    @classmethod
    def table(cls) -> str:
        return cls.TABLE or cls.class_name()
    
    @classmethod
    def item_name(cls) -> str:
        """ITEM_NAME or slug of table name"""
        return cls.ITEM_NAME or slug(cls.table())
    
    @property
    def get_key(self) -> str:
        return getattr(self, 'key', None)
    

