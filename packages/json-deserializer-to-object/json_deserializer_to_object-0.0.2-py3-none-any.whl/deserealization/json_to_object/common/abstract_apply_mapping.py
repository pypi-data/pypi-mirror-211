from __future__ import annotations

import json
from abc import ABC
from typing import List

from deserealization.json_to_object.contract.interface_mapping import IApplyMapping
from deserealization.typing import JsonToObjectType

ENCODING = "utf-8"


class AbstractApplyMapping(IApplyMapping, ABC):
    @staticmethod
    def read_json(path: str) -> str:
        """ Get string from file"""
        with open(path, encoding=ENCODING) as json_file:
            mapping_str = json.loads(json_file.read())
        return mapping_str

    @classmethod
    def get(cls, path: str, model: JsonToObjectType, skip_undefined_json_field: bool) -> \
            List | JsonToObjectType:
        return cls.transform_json_to_object(cls.read_json(path), model, skip_undefined_json_field)
