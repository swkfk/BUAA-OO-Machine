
from src.core.requests.UrlGenerator import URL
from src.core.requests.CommonRequests import Get


def GetHistoryList(user_name: str):
    return Get(URL.HistoryView(user_name))
