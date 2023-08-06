from __future__ import annotations

import enum

from deserealization.json_to_object.implementation.generic_json2object import GenericJson2Object
from deserealization.json_to_object.implementation.json2object import Json2Object
from deserealization.typing import TypeForData, JsonToObjectType


class EnumJson2ObjectFactory(enum.Enum):
    json2Object = Json2Object
    generic_json2object = GenericJson2Object


class Json2ObjectFactory:
    def __init__(self, enum_json_to_object: EnumJson2ObjectFactory, data: TypeForData,
                 model: JsonToObjectType, skip_undefined_json_field: bool):
        self.enum_json_to_object = enum_json_to_object
        self.data = data
        self.model = model
        self.skip_undefined_json_field = skip_undefined_json_field

    def __call__(self, *args, **kwargs):
        return self.enum_json_to_object.value(self.data, self.model, self.skip_undefined_json_field)
