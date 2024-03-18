import asyncio

from fastapi import APIRouter, WebSocket

from core.checker_core import GetDiffSame
from core.fs import JsonLoader, DB_ROOT, COURSE_ROOT, USER_ROOT, GetPointTimestamp, POINT_ROOT, GetPointEnable
from core.point_cacher import PushPointData, PopPointData

router = APIRouter()


@router.get("/proj")
async def GetProjList():
    """
    获取项目全部项目（Project）列表
    :return: 由字符串组成的列表，每个元素即为项目名，有序
    """
    obj = await JsonLoader(DB_ROOT / "course.json")
    return [p["title"] for p in obj]


@router.get("/unit")
async def GetUnitList(proj: int):
    """
    获取指定项目的全部单元（Unit）列表
    :param proj: 项目的 **编号**， 从 0 开始计数
    :return: 该项目的全部单元组成的列表，每个元素即为单元名，有序
    """
    obj = await JsonLoader(DB_ROOT / "course.json")
    # TODO /// Error handler (Index out of the boundary)
    return [u["title"] for u in obj[proj]["units"]]


@router.websocket("/point/{user}/{proj}/{unit}")
async def GetPointList(ws: WebSocket, user: str, proj: int, unit: int):
    """
    获取某个用户对于某一项目、某一单元的测试点信息
    :param ws: WebSocket 连接
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    """
    unit_path = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_path)
    lst = []
    await ws.accept()
    await ws.send_text(str(len(unit_obj)))
    for point_idx, point in enumerate(unit_obj):
        await ws.send_text(str(point_idx + 1))
        if not await GetPointEnable(proj, unit, point_idx):
            lst.append({
                "same": [], "diff": [],
                "desc": point["desc"],
                "ret_desc": "",
                "disabled": True
            })
            continue
        timestamp = await GetPointTimestamp(proj, unit, point_idx)
        ret_file = POINT_ROOT / f"{timestamp}" / "return_value" / user
        if ret_file.exists():
            ret = ret_file.read_text()
        else:
            ret = "<Not Submit Yet>"
        if not ret.startswith("<"):
            ret = "Return Value: " + ret
        same, diff = await GetDiffSame(proj, unit, point_idx, user)
        lst.append({
            "same": same, "diff": diff,
            "desc": point["desc"],
            "ret_desc": ret
        })
        await asyncio.sleep(0.01)  # How dare it?
    PushPointData(user, proj, unit, lst)
    await ws.send_text("-1")

@router.get("/point")
async def GetPointList(user: str, proj: int, unit: int):
    return PopPointData(user, proj, unit)

@router.get("/history")
async def GetHistoryList(user: str):
    """
    返回某个用户的历史提交信息，不区分项目与单元
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :return: 列表，每个元素为给用户的一次提交，有序。对于每次提交的字典，包含如下键：
        "digest": str,  该次提交的代码摘要（md5 算法）
        "time": str,    该次提交的时间（格式为 "%Y-%m-%d %H:%M"）
    """
    user_file = USER_ROOT / f"{user}.json"
    if not user_file.exists():
        user_file.write_text("[]")
    return await JsonLoader(user_file)
