from src.core.requests.CommonRequests import Get
from src.core.requests.UrlGenerator import URL


def GetProjList():
    return Get(URL.ProjList())


def GetUnitList(proj_id: int):
    return Get(URL.UnitList(proj_id))


def GetPointInfo(user_name: str, proj_id: int, unit_id: int):
    return Get(URL.PointList(user_name, proj_id, unit_id))
