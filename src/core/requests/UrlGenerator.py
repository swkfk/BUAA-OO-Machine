from src.core.settings.ServerConfig import server_config


class URL:
    @staticmethod
    def BaseUrl():
        return f"{server_config['url']}:{server_config['port']}"

    @staticmethod
    def HistoryView(user_name: str):
        return f"{URL.BaseUrl()}/history?user={user_name}"
