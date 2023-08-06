from __future__ import annotations

from abc import abstractmethod, ABCMeta
from typing import List

from deserealization.typing import JsonToObjectType


class IApplyMapping(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def read_json(path: str) -> str:
        """ Get string from file"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def transform_json_to_object(mapping_str: str, model: JsonToObjectType, skip_undefined_json_field: bool):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(cls, path: str, model: JsonToObjectType, skip_undefined_json_field: bool) -> \
            List | JsonToObjectType:
        raise NotImplementedError
