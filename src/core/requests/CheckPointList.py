from src.core.requests.CommonRequests import callback_handler as __handler
from src.core.requests.UrlGenerator import URL


def GetProjList(aux):
    __handler(aux, URL.ProjList())


def GetUnitList(aux, proj_id: int):
    __handler(aux, URL.UnitList(proj_id))


def GetPointInfo(aux, user_name: str, proj_id: int, unit_id: int):
    __handler(aux, URL.PointList(user_name, proj_id, unit_id))
