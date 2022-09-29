import datetime as dt
import pathlib

from fastapi import APIRouter
from api.utils import get_version, Health, Version
from config.base import settings

router = APIRouter()


@router.get("/health/", response_model=Health)
async def health() -> Health:
    return Health(date=dt.datetime.utcnow().isoformat())


@router.get("/version/", response_model=Version)
async def version() -> Version:
    _version = get_version(pathlib.Path(settings.REPO_ROOT / "REVISION"))
    return Version(branch=_version.branch, version=_version.version)
