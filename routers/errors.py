from fastapi import APIRouter

from core.fs import JAVA_ROOT

router = APIRouter()


@router.get("/errors/compile")
def GetCEMsg(digest: str):
    text = (JAVA_ROOT / f"{digest}" / "compile-msg.txt").read_text()
    return text.replace(f"database/java/{digest}/", "")
