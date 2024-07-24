from src.core.settings.GlobalSettings import Globals

_lang_config = Globals("i18n")

_lang_code = None


def get_lang():
    global _lang_code
    if _lang_code is None:
        if "code" in _lang_config:
            _lang_code = _lang_config["code"]
        else:
            _lang_code = "en"
    return _lang_code


def set_lang(lang):
    global _lang_code
    _lang_config["code"] = lang
    _lang_code = lang


def have_lang():
    return "code" in _lang_config and _lang_config["code"] is not None and _lang_config["code"] != ""
