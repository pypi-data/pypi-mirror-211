"""
Mapping json file to an Object Method
"""
from __future__ import annotations

from typing import List

from deserealization.typing import JsonToObjectType
from deserealization.json_to_object.common.abstract_apply_mapping import AbstractApplyMapping
from deserealization.json_to_object.implementation.json2object_factory import Json2ObjectFactory, EnumJson2ObjectFactory


class ApplyJsonMapping(AbstractApplyMapping):
    @staticmethod
    def transform_json_to_object(mapping_str: str, model: JsonToObjectType, skip_undefined_json_field: bool) \
            -> List | JsonToObjectType:
        json_to_object_factory = Json2ObjectFactory(enum_json_to_object=EnumJson2ObjectFactory.json2Object,
                                                    data=mapping_str, model=model,
                                                    skip_undefined_json_field=skip_undefined_json_field)
        return json_to_object_factory().build()


class ApplyGenericJsonMapping(AbstractApplyMapping):
    @staticmethod
    def transform_json_to_object(mapping_str: str, model: JsonToObjectType, skip_undefined_json_field: bool) \
            -> List | JsonToObjectType:
        json_to_object_factory = Json2ObjectFactory(enum_json_to_object=EnumJson2ObjectFactory.generic_json2object,
                                                    data=mapping_str, model=model,
                                                    skip_undefined_json_field=skip_undefined_json_field)
        return json_to_object_factory().build()
