from . import i18n
from src.core.settings.I18nConfig import get_lang

_i18n = i18n.I18nRoot(get_lang)

# Expose to the Caller
HistoryDialog = _i18n.HistoryDialog.Strings
MainWidget = _i18n.MainWidget.Strings
PointArea = _i18n.PointArea.Strings
RegisterDialog = _i18n.RegisterDialog.Strings
SettingDialog = _i18n.SettingDialog.Strings
SubmitDialog = _i18n.SubmitDialog.Strings
UploadDialog = _i18n.UploadDialog.Strings

# Expose to the Setting Dialog
lang_list = [
    ('en', "English"),
    ('zh-CN', "简体中文")
]
