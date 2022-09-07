import datetime
from pathlib import Path
from pydantic import BaseModel
from typing import Any, NamedTuple, Optional


class ErrorModel(BaseModel):
    message: str
    errors: Any
    code: Optional[str]
    error_code: Optional[str]
    key: Optional[str]


class Health(BaseModel):
    date: datetime.datetime


class Version(NamedTuple):
    branch: str
    version: str


def get_version(revision_file: Path) -> Version:
    if not revision_file.is_file():
        raise Exception("Could not find a REVISION file")
    with revision_file.open("r") as f:
        line = f.readline()
        return Version(*line.strip().rsplit(" ", 1))
