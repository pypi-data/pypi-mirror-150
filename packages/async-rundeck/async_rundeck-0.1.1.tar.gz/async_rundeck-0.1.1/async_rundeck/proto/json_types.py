import json
from typing import TypeVar, NewType

T = TypeVar("T")

Number = float
String = str
Boolean = bool
Integer = int
Object = dict

__all__ = ["Number", "String", "Boolean", "Integer", "Object"]
