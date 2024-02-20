from src.core.settings.GlobalSettings import Globals

_lang_config = Globals("i18n")

_lang_code = None


def get_lang():
    global _lang_code
    if _lang_code is None:
        if "code" not in _lang_config:
            _lang_config["code"] = 'en'
        _lang_code = _lang_config["code"]
    return _lang_code


def set_lang(lang):
    _lang_config["code"] = lang
