from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict

from deserealization.typing import IDataClass, JsonToObjectType


class IJson2Object(ABC):

    @staticmethod
    @abstractmethod
    def model_and_data_validator(data: Dict, model: JsonToObjectType, skip_undefined_json_field: bool):
        """
        method to implement in subclass
        Returns
        -------
        """
        raise NotImplementedError("To be implemented to validate data")

    @abstractmethod
    def deserialize_list_data(self, data: List) -> List | IDataClass:
        """
        method to implement in subclass with list
        Returns
        -------
        """
        raise NotImplementedError("To be implemented to list type")

    @abstractmethod
    def deserialize_dict_data(self, data: Dict) -> List | JsonToObjectType:
        """
        method to implement in subclass with dict
        Returns
        -------
        """
        raise NotImplementedError("To be implemented to dict type")

    @abstractmethod
    def deserialize_str_data(self, data: str) -> List | JsonToObjectType:
        """
        method to implement in subclass with string
        Returns
        -------
        """
        raise NotImplementedError("To be implemented to string type")

    @abstractmethod
    def build(self) -> List | JsonToObjectType:
        """
        method to fill model and build Object
        Returns
        -------
        """
        raise NotImplementedError("To be implemented to render model fill with data from json file")
