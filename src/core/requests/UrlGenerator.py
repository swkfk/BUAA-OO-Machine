from src.core.settings.ServerConfig import server_config


class URL:
    @staticmethod
    def BaseUrl():
        return f"{server_config['url']}:{server_config['port']}"

    @staticmethod
    def HistoryView(user_name: str):
        return f"{URL.BaseUrl()}/history?user={user_name}"

    @staticmethod
    def ProjList():
        return f"{URL.BaseUrl()}/proj"

    @staticmethod
    def UnitList(proj_id: int):
        return f"{URL.BaseUrl()}/unit?proj={proj_id}"

    @staticmethod
    def PointList(user_name: str, proj_id: int, unit_id: int):
        return f"{URL.BaseUrl()}/point?user={user_name}&proj={proj_id}&unit={unit_id}"

    @staticmethod
    def DownloadSource(digest: str):
        return f"{URL.BaseUrl()}/src?digest={digest}"
