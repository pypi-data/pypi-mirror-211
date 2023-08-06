from __future__ import annotations

import enum
from typing import List
from dataclasses import dataclass, field
from deserealization.typing import IDataClass


@dataclass
class Mapping(IDataClass):
    type: str = field(default=str())
    data_type: str = field(default=str())
    source_field: str = field(default=str())
    target_field: str = field(default=str())
    action: str = field(default=str())


@dataclass
class Entity(IDataClass):
    entity_name: str = field(default=str())
    mappings: List[Mapping] = field(default_factory=lambda: [Mapping()])


@dataclass
class Json(IDataClass):
    source_name: str = field(default=str())
    entities: List[Entity] = field(default_factory=lambda: [Entity()])


@dataclass
class MappingWithRequiredField(IDataClass):
    type: str = field(default=str())
    data_type: str = field(default=str())
    source_field: str = field(default=str())
    target_field: str = field(default=str())
    action: str = field(default=str(), metadata={'required':False})


@dataclass
class EntityWithRequiredField(IDataClass):
    entity_name: str = field(default=str())
    mappings: List[MappingWithRequiredField] = field(default_factory=lambda: [MappingWithRequiredField()])


@dataclass
class JsonWithRequiredField(IDataClass):
    source_name: str = field(default=str())
    entities: List[EntityWithRequiredField] = field(default_factory=lambda: [EntityWithRequiredField()])


@dataclass
class EntityWithListFiled(IDataClass):
    entity_name: str = field(default=str())
    tags: List[str | int] = field(default_factory=lambda: [str()])
    three_last_prices: List[float] = field(default_factory=lambda: [float()])
    code_numbers: List[int] = field(default_factory=lambda: [int()])
    mappings: List[Mapping] = field(default_factory=lambda: [Mapping()])


@dataclass
class JsonWithEntityTagged(IDataClass):
    source_name: str = field(default="")
    entities: List[EntityWithListFiled] = field(default_factory=lambda: [EntityWithListFiled()])


class EnumJsonModel(enum.Enum):
    json = Json()
    json_with_required_fields = JsonWithRequiredField()
    json_with_entity_tagged = JsonWithEntityTagged()
