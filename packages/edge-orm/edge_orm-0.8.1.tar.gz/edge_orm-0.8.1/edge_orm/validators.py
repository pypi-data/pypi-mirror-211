import typing as T
from pydantic import BaseModel, FieldValidationInfo
from devtools import debug
from enum import Enum

ModelType = T.TypeVar("ModelType", bound=BaseModel)
EnumType = T.TypeVar("EnumType", bound=Enum)


def transform_enum(
    original_value: str | Enum,
    new_enum_type: T.Type[EnumType],
    ignore_null: bool = False,
) -> T.Optional[EnumType]:
    if ignore_null:
        if original_value is None:
            return None
    if isinstance(original_value, Enum):
        og_val = original_value.value
    else:
        og_val = original_value
    new_value = (
        og_val.replace("/", "").replace("-", "_").replace("  ", " ").replace(" ", "_")
    )
    return new_enum_type(new_value)


def enum_from_str(
    cls: T.Type[BaseModel], v: EnumType | str, info: FieldValidationInfo
) -> EnumType | None:
    # idk who uses this
    field = cls.model_fields[info.field_name]
    debug(field)
    if isinstance(v, str) or not isinstance(v, field.type_):
        return transform_enum(original_value=v, new_enum_type=field.type_)
    else:
        return v
