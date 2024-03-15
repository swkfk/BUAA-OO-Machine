from fastapi import APIRouter

from core.checker_core import GetDiffSame
from core.fs import JsonLoader, DB_ROOT, COURSE_ROOT, USER_ROOT, GetPointTimestamp, POINT_ROOT, GetPointEnable

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


@router.get("/point")
async def GetPointList(user: str, proj: int, unit: int):
    """
    获取某个用户对于某一项目、某一单元的测试点信息
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :return: 列表，每个元素为一个测试点的信息，有序。对于每个测试点的字典，包含如下键：
        "same": [str],  结果相同的用户名称的列表
        "diff": [str],  结果不同的用户名称的列表
        "desc": str,    该测试点的描述
    """
    unit_path = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    unit_obj = await JsonLoader(unit_path)
    lst = []
    for point_idx, point in enumerate(unit_obj):
        if not await GetPointEnable(proj, unit, point_idx):
            lst.append({
                "same": ['Disabled!'], "diff": [],  # For old-version front-end
                "desc": point["desc"],
                "ret_desc": "Return Value: 0",
                "disabled": True  # For new-version front-end
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
    return lst


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
