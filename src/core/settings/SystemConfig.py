import qdarkstyle

from src.core.settings.GlobalSettings import Globals

_sys_config = Globals("system")

LIGHT_THEME = "light"
DARK_THEME = "dark"


def get_theme():
    if "theme" not in _sys_config:
        _sys_config["theme"] = LIGHT_THEME
    if _sys_config["theme"] == LIGHT_THEME:
        return qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=qdarkstyle.LightPalette)
    if _sys_config["theme"] == DARK_THEME:
        return qdarkstyle.load_stylesheet(qt_api='pyqt6', palette=qdarkstyle.DarkPalette)
    return ""  # TODO /// Error Handler


def is_dark_theme():
    return _sys_config["theme"] == DARK_THEME


def set_theme(s):
    _sys_config["theme"] = s
