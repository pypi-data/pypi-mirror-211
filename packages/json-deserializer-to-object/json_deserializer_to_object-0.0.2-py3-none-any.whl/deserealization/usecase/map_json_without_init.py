from __future__ import annotations
import enum
from typing import List, Type
from dataclasses import dataclass, field
from deserealization.typing import IDataClass


@dataclass
class Mapping(IDataClass):
    type: str
    data_type: str
    source_field: str
    target_field: str
    action: str


@dataclass
class Entity(IDataClass):
    entity_name: str
    mappings: List[Type[Mapping]] = field(default_factory=lambda: [Mapping])


@dataclass
class Json(IDataClass):
    source_name: str
    entities: List[Type[Entity]] = field(default_factory=lambda: [Entity])


@dataclass
class MappingWithRequiredField(IDataClass):
    type: str
    data_type: str
    source_field: str
    target_field: str
    action: str = field(metadata={'required':False})


@dataclass
class EntityWithRequiredField(IDataClass):
    entity_name: str
    mappings: List[Type[MappingWithRequiredField]] = field(default_factory=lambda: [MappingWithRequiredField])


@dataclass
class JsonWithRequiredField(IDataClass):
    source_name: str
    entities: List[Type[EntityWithRequiredField]] = field(default_factory=lambda: [EntityWithRequiredField])


@dataclass
class EntityWithListFiled(IDataClass):
    entity_name: str
    tags: List[str | int]
    three_last_prices: List[float]
    code_numbers: List[int]
    mappings: List[Type[Mapping]] = field(default_factory=lambda: [Mapping])


@dataclass
class JsonWithEntityTagged(IDataClass):
    source_name: str
    entities: List[Type[EntityWithListFiled]] = field(default_factory=lambda: [EntityWithListFiled])


class EnumGenericJsonModel(enum.Enum):
    json = Json
    json_with_required_fields = JsonWithRequiredField
    json_with_entity_tagged = JsonWithEntityTagged
