import typing as T
from pydantic import BaseModel
import json


def to_basemodel(v: str | BaseModel | None, cls: T.Type[BaseModel]) -> BaseModel | None:
    if isinstance(v, str):
        if v == "null":
            return None
        return cls(**json.loads(v))
    return v
