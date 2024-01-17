
def GetHistoryList(user_name: str, callback):
    """
    TODO: Request from the server
    :param callback: be given the required data
    :param user_name: shall *NOT* be the __TEMP__
    :return: The list of the history, each elem is a dict with the digest and the submit time
    """
    callback([
        {"digest": "81be9440009828e57d444ece8c07959a", "time": "2023-12-31 23:59"},
        {"digest": "64db716d64f0c4c93e950a039960a835", "time": "2024-01-01 23:59"},
        {"digest": "01a4fe1c18c325a9aae80249d608ef6c", "time": "2024-01-02 23:59"},
    ])
