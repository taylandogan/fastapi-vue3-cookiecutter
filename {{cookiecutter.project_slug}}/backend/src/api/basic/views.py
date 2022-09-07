import datetime as dt
import pathlib

from fastapi import APIRouter
from utils import get_version, Health, Version
from config.base import app_settings as settings

router = APIRouter()


@router.get("/health/", response_model=Health)
async def health() -> Health:
    return Health(date=dt.datetime.utcnow().isoformat())


@router.get("/version/", response_model=Version)
async def version() -> Version:
    _version = get_version(pathlib.Path(settings.REPO_ROOT / "REVISION"))
    return Version(branch=_version.branch, version=_version.version)
