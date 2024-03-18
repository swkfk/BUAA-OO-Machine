from fastapi import APIRouter

from core.fs import DB_ROOT

router = APIRouter()


@router.get("/upgrade")
def AskVersion():
    version_file = DB_ROOT / "version"
    if not version_file.exists():
        return "0"
    return version_file.read_text().strip()
