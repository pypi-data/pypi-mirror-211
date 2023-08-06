from __future__ import annotations

from abc import ABC
from dataclasses import Field
from typing import Dict, Optional, List

from deserealization.json_to_object.contract.interface_json_to_object import IJson2Object
from deserealization.typing import TypeForData, JsonToObjectType


class AbstractJson2Object(IJson2Object, ABC):
    def __init__(self, data: TypeForData):
        self.data = data

    @classmethod
    def model_and_data_validator(cls, data: Dict, model: JsonToObjectType,
                                 skip_undefined_json_field: bool) -> None:
        if isinstance(model, (str, float, int, bool)):
            return
        data_keys = list(data.keys())
        model_attributes = list(model.__dataclass_fields__.keys())
        if diff_field := list(set(model_attributes) - set(data_keys)):
            for field in diff_field:
                field_value: Optional[Field] = model.__dataclass_fields__.get(field)
                if _ := (field_value.metadata.get("required") in [None, True]) if field_value else False:
                    raise ValueError(f"Field not match. Some field are missing: {diff_field}. If this field is not "
                                     f"required, in dataclass field, add option metadata=dict(required=False).")
        diff_field_from_json = list(set(data_keys) - set(model_attributes))
        if diff_field_from_json and not skip_undefined_json_field:
            raise ValueError(f"Field not match. There are too many field in json file compare to model."
                             f" Those flied are {diff_field_from_json}. To skip undefined json field, put "
                             f"parameter skip_undefined_json_field=True")

    def build(self) -> List | JsonToObjectType:
        """
        Returns a model or a list of model
        -------
        """
        if isinstance(self.data, list):
            return self.deserialize_list_data(self.data)
        if isinstance(self.data, dict):
            return self.deserialize_dict_data(self.data)
        if isinstance(self.data, str):
            return self.deserialize_str_data(self.data)
        raise ValueError("data most be dict or list or str deserializable")
