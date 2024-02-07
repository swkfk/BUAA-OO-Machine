from src.core.requests.CommonRequests import callback_handler as __handler
from src.core.requests.UrlGenerator import URL


def GetHistoryList(aux, user_name: str):
    __handler(aux, URL.HistoryView(user_name))
