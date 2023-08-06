from dataclasses import Field
from typing import Protocol, Dict, Union, runtime_checkable,Type

UnionBasicType = Union[str, float, int, bool]
TypeForData = Union[list, dict, UnionBasicType]


@runtime_checkable
class IDataClass(Protocol):
    __dataclass_fields__: Dict[str, Field]


IDataClassUnionBasicType = Union[IDataClass, UnionBasicType]
TypeDataclassUnionBasicType = Union[UnionBasicType, Type[IDataClass]]
JsonToObjectType = Union[Type[IDataClass], IDataClass, UnionBasicType]
