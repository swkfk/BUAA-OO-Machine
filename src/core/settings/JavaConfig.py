from src.core.settings.GlobalSettings import Globals

_java_config = Globals("java")


def get_main_class():
    if "main-class" not in _java_config:
        _java_config["main-class"] = ""
    return _java_config["main-class"]


def set_main_class(main):
    _java_config["main-class"] = main


def get_ask_each():
    if "ask-each" not in _java_config:
        _java_config["ask-each"] = True
    return str(_java_config["ask-each"]).lower() == "true"


def set_ask_each(b):
    _java_config["ask-each"] = bool(b)


def set_not_ask_each():
    _java_config["ask-each"] = False
