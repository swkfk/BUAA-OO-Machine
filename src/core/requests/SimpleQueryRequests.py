import base64

from src.core.requests.CommonRequests import callback_handler as __handler
from src.core.requests.UrlGenerator import URL


def GetProjList(aux):
    __handler(aux, URL.ProjList())


def GetUnitList(aux, proj_id: int):
    __handler(aux, URL.UnitList(proj_id))


def GetPointInfo(aux, user_name: str, proj_id: int, unit_id: int):
    __handler(aux, URL.PointList(user_name, proj_id, unit_id))


def GetPointREMsg(aux, user_name: str, proj_id: int, unit_id: int, point_id: int):
    __handler(aux, URL.REMsg(user_name, proj_id, unit_id, point_id))

def SetPointStatus(aux, proj_id: int, unit_id: int, point_id: int, disabled: bool):
    __handler(aux, URL.SetPointStatus(proj_id, unit_id, point_id, disabled))

def SetPointDesc(aux, proj_id: int, unit_id: int, point_id: int, desc: str):
    __handler(aux, URL.ModifyDesc(proj_id, unit_id, point_id,
                                  base64.urlsafe_b64encode(desc.encode('utf-8')).decode('utf-8')))

def ConnectTest(aux):
    __handler(aux, URL.ConnTest())


def GetNewVersion(aux):
    __handler(aux, URL.CheckUpgrade())
