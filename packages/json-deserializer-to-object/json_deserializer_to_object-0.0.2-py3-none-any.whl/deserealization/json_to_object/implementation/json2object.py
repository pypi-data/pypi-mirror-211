from __future__ import annotations

import copy
import json
from typing import List, Dict
from dataclasses import is_dataclass

from deserealization.json_to_object.common.data_validation_applementation import AbstractJson2Object
from deserealization.typing import IDataClass, IDataClassUnionBasicType, TypeForData, JsonToObjectType


class Json2Object(AbstractJson2Object):
    """
    class how allow to convert json to defined object
    :data: is a dict or list or string to map
    :model: is the object model to use for deserialization
    """

    def __init__(self, data: TypeForData, model: IDataClassUnionBasicType, skip_undefined_json_field: bool = False):
        if not data or isinstance(data, str) and not data.strip():
            raise ValueError('The data most not to be null or empty.')
        if not is_dataclass(model) and not isinstance(model, (str, float, int, bool)):
            raise ValueError('The model most be a dataclass.')
        if isinstance(data, dict):
            self.model_and_data_validator(data, model, skip_undefined_json_field)
        self.data = data
        self.model: IDataClassUnionBasicType = model if isinstance(model, str) else copy.copy(model)
        self.skip_undefined_json_field = skip_undefined_json_field
        super().__init__(data)

    def deserialize_list_data(self, data: List) -> List | IDataClass:
        """
        Parameters
        ----------
        data: data of type list
        Returns list of model
        -------
        """
        if isinstance(self.model, (str, float, int, bool)):
            return data
        return [Json2Object(d, self.model, self.skip_undefined_json_field).build() for d in data]

    def deserialize_dict_data(self, data: Dict) -> List | JsonToObjectType:
        """
        Parameters
        ----------
        data: of type dict
        Returns model
        -------
        """
        for key, value in data.items():
            if hasattr(self.model, key):
                attr = getattr(self.model, key)
                if isinstance(value, (dict, list)):
                    sub_model = attr[-1] if isinstance(value, list) else attr
                    result = Json2Object(value, sub_model, self.skip_undefined_json_field).build()
                else:
                    result = value
                setattr(self.model, key, result)
        return self.model

    def deserialize_str_data(self, data: str) -> List | JsonToObjectType:
        """
        Parameters
        ----------
        data: if data is str convert to json object dict
        Returns
        -------
        """
        return Json2Object(json.loads(data), self.model, self.skip_undefined_json_field).build()
