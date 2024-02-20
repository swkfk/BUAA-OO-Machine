class I18nRoot:
    _lang_getter = None

    def __init__(self, lang_getter):
        self._lang_getter = lang_getter

    def __getattr__(self, item):
        _lang_code = self._lang_getter()  # Cache in the getter
        return __import__(f"src.i18n.{_lang_code}.{item}", fromlist=['src', 'i18n', _lang_code])

