from __future__ import annotations

__all__ = ['BaseCollection', 'BaseContext', 'Singleton']

from abc import ABC, abstractmethod
from typing import Union
from collections import ChainMap, UserList, UserString, UserDict



class BaseContext(ChainMap):
    pass


class BaseCollection(ABC):
    def __init__(self, *args, **kwargs):
        self.args = [*args]
        self.kwargs = kwargs
        super().__init__(self.init_data())
        assert isinstance(self, (UserString, UserDict, UserList, set))
    
    @abstractmethod
    def init_data(self) -> Union[str, dict, list, set]:
        return NotImplemented


class Singleton(ABC):
    _this = None
    
    @abstractmethod
    def __new__(cls, *args, **kwargs):
        if cls._this is None:
            cls._this = super().__new__(cls, *args, **kwargs)
        return cls._this


