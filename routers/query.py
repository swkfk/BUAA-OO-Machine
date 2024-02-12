from fastapi import APIRouter

from core.fs import JsonLoader, DB_ROOT, COURSE_ROOT

router = APIRouter()


@router.get("/proj")
async def GetProjList():
    """
    获取项目全部项目（Project）列表
    :return: 由字符串组成的列表，每个元素即为项目名，有序
    """
    obj = await JsonLoader(DB_ROOT / "course.json")
    return list(map(lambda x: x["title"], obj))


@router.get("/unit")
async def GetUnitList(proj: int):
    """
    获取指定项目的全部单元（Unit）列表
    :param proj: 项目的 **编号**， 从 0 开始计数
    :return: 该项目的全部单元组成的列表，每个元素即为单元名，有序
    """
    obj = await JsonLoader(DB_ROOT / "course.json")
    # TODO /// Error handler (Index out of the boundary)
    return obj[proj]["units"]


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
        lst.append({
            "same": [], "diff": [],  # TODO ///
            "desc": point["desc"]
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
    pass
