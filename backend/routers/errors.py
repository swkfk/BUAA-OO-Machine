import html

from fastapi import APIRouter

from core.fs import JAVA_ROOT, GetPointTimestamp, POINT_ROOT

router = APIRouter()


@router.get("/errors/compile")
async def GetCEMsg(digest: str):
    text = (JAVA_ROOT / f"{digest}" / "compile-msg.txt").read_text()
    return html.escape(text.replace(f"database/java/{digest}/", ""))


@router.get("/errors/runtime")
async def GetREMsg(user: str, proj: int, unit: int, point: int):
    timestamp = await GetPointTimestamp(proj, unit, point)
    try:
        ret = (POINT_ROOT / f"{timestamp}" / "return_value" / user).read_text()
        text = (POINT_ROOT / f"{timestamp}" / "stderr" / user).read_text()
    except FileNotFoundError:
        ret = "<Not Submit Yet>"
        text = ""
    return f"<pre><b>Return Value: {html.escape(ret)}</b><br />{html.escape(text)}</pre>"
