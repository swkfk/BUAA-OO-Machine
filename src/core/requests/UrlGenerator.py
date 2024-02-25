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
    def REMsg(user_name: str, proj_id: int, unit_id: int, point_id: int):
        return f"{URL.BaseUrl()}/errors/runtime?user={user_name}&proj={proj_id}&unit={unit_id}&point={point_id}"

    @staticmethod
    def DownloadSource(digest: str):
        return f"{URL.BaseUrl()}/src?digest={digest}"

    @staticmethod
    def ConnTest():
        return f"{URL.BaseUrl()}/"

    @staticmethod
    def Status(digest: str):
        return f"{URL.BaseUrl()}/status?digest={digest}"

    @staticmethod
    def Submit(user: str, proj: int, unit: int, class_base64: str, passwd: str = None, salt: str = None):
        if passwd is None or salt is None:
            return f"{URL.BaseUrl()}/submit?user={user}&proj={proj}&unit={unit}&class_b64={class_base64}"
        return f"{URL.BaseUrl()}/submit?user={user}&proj={proj}&unit={unit}&" \
               f"class_b64={class_base64}&passwd={passwd}&salt={salt}"

    @staticmethod
    def CEMsg(digest: str):
        return f"{URL.BaseUrl()}/errors/compile?digest={digest}"

    @staticmethod
    def Upload(proj: int, unit: int, desc_base64: str):
        return f"{URL.BaseUrl()}/upload?proj={proj}&unit={unit}&desc={desc_base64}"

    @staticmethod
    def DownloadInout(scope: str, user: str, proj: int, unit: int, point: int):
        return f"{URL.BaseUrl()}/{scope}?user={user}&proj={proj}&unit={unit}&point={point}"

    @staticmethod
    def CheckUpgrade():
        return f"{URL.BaseUrl()}/upgrade"
