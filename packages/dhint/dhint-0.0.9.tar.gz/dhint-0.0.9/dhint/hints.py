__all__ = [
        'JsonPrimitive',
        'DetaKey',
        'Jsonable',
        'JsonSequence',
        'Types',
        'TypeArgs',
        'TupleMapTypes',
        'TupleSequenceTypes',
        'ParserEntry',
        'ParserResult',
        'GenericType',
        'Number',
        'ParserReturn',
]

import datetime
from decimal import Decimal
from collections import ChainMap, deque, UserDict, UserList
from typing import Union, TypeVar

JsonPrimitive = Union[str, float, int, bool, None]
DetaKey = Union[str, None]
JsonSequence = list[JsonPrimitive]
JsonDict = dict[str, Union[JsonSequence, JsonPrimitive]]
Jsonable = Union[JsonDict, JsonSequence, JsonPrimitive]
TypeArgs = tuple[type]
Types = Union[type, TypeArgs]
TupleSequenceTypes = (tuple, list, set, deque, UserList)
TupleMapTypes = (dict, UserDict, ChainMap)
ParserEntry = TypeVar('ParserEntry')
ParserResult = TypeVar('ParserResult')
ParserReturn = Union[ParserEntry, ParserResult]
GenericType = TypeVar('GenericType')
Number = TypeVar('Number', float, int, Decimal)
