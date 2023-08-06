from __future__ import annotations

import json
from dataclasses import is_dataclass, MISSING, Field
from typing import Dict, List

from deserealization.typing import IDataClass, JsonToObjectType
from deserealization.json_to_object.common.data_validation_applementation import AbstractJson2Object


class GenericJson2Object(AbstractJson2Object):
    def __init__(self, data, model: JsonToObjectType, skip_undefined_json_field: bool):
        if not data or isinstance(data, str) and not data.strip():
            raise ValueError('The data most not to be null or empty.')
        if not is_dataclass(model) and not isinstance(model, (str, float, int, bool)):
            raise ValueError('The model most be a dataclass.')
        if isinstance(data, dict) and isinstance(model, type) and isinstance(model, IDataClass):
            self.model_and_data_validator(data, model, skip_undefined_json_field)
        self.model: JsonToObjectType = model
        self.skip_undefined_json_field: bool = skip_undefined_json_field
        self.data = data
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
        return [GenericJson2Object(d, self.model, self.skip_undefined_json_field).build() for d in data]

    @staticmethod
    def from_data_dict_fill_missing_field(data: Dict, model_fields: Dict[str, Field],
                                          dict_key_value_mapped: Dict) -> Dict:
        for key in model_fields:
            if model_field := model_fields.get(key):
                metadata_for_model = model_field.metadata.get("required")
            else:
                metadata_for_model = None
            if key not in data.keys() and metadata_for_model is False:
                dict_key_value_mapped.update({key: ""})
        return dict_key_value_mapped

    def deserialize_dict_data(self, data: Dict) -> List | JsonToObjectType:
        """
        Parameters
        ----------
        data: of type dict
        Returns model
        -------
        """
        if isinstance(self.model, (str, float, int, bool)):
            return self.model
        dict_key_value_mapped: Dict = {}
        model_fields: Dict[str, Field] = self.model.__dataclass_fields__
        for key, value in data.items():
            if model_in_key := model_fields.get(key):
                model_from_default_factory = model_in_key.default_factory
                if isinstance(value, (dict, list)) and model_from_default_factory is not MISSING:
                    default_factory_call = model_from_default_factory()
                    attr = default_factory_call[-1] if isinstance(value, list) else default_factory_call

                    result = GenericJson2Object(value, attr, self.skip_undefined_json_field).build()

                else:
                    result = value
                dict_key_value_mapped.update({key: result})
        dict_key_value_mapped = self.from_data_dict_fill_missing_field(data, model_fields, dict_key_value_mapped)
        # IDataClass is interface: no callable, call will do in concrete dataclass
        return self.model(**dict_key_value_mapped)  # type: ignore

    def deserialize_str_data(self, data: str) -> List | JsonToObjectType:
        """
        Parameters
        ----------
        data: if data is str convert to json object dict
        Returns
        -------
        """
        return GenericJson2Object(json.loads(data), self.model, self.skip_undefined_json_field).build()
