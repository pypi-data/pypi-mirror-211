"""
This main file is dedicated for the use-case example.
"""

from __future__ import annotations

from typing import List, Union
import pkg_resources

from deserealization import ApplyJsonMapping, ApplyGenericJsonMapping
from deserealization.typing import IDataClass
from deserealization.usecase.map_json import Json, JsonWithRequiredField, JsonWithEntityTagged, EnumJsonModel
from deserealization.usecase.map_json_without_init import EnumGenericJsonModel

UnionType = Union[JsonWithEntityTagged, Json, JsonWithRequiredField]


def get_json_to_object(json_file_path: str, model_enum: EnumJsonModel, skip_undefined_json_field: bool = False) -> \
        List | UnionType:
    model_value: IDataClass = model_enum.value
    json_absolute_path_customers = pkg_resources \
        .resource_filename(__name__, json_file_path)
    return ApplyJsonMapping.get(path=json_absolute_path_customers, model=model_value,
                                skip_undefined_json_field=skip_undefined_json_field)  # type: ignore


def get_generic_json_to_object(json_file_path: str, model_enum: EnumGenericJsonModel,
                               skip_undefined_json_field: bool = False) -> \
        List | UnionType:
    json_absolute_path_customers = pkg_resources \
        .resource_filename(__name__, json_file_path)
    return ApplyGenericJsonMapping.get(path=json_absolute_path_customers, model=model_enum.value,
                                       skip_undefined_json_field=skip_undefined_json_field)  # type: ignore
