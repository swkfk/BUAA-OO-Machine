class Strings:
    class Widget:
        Index = "#{}"
        Same = "Same with {} person(s)"
        Diff = "Differ from {} person(s)"

        @staticmethod
        def ToolTip(lst):
            return "".join((f"<li>{p}</li>" for p in lst))

    class Download:
        Input = "Save Stdin"
        Output = "Save Stdout"
        Others = "Save others' Stdout"

        Dict = {
            "input": Input,
            "output": Output,
            "all": Others
        }

    class Bar:
        Download = "Downloading ..."
        ReadMsg = "Getting the message ..."
        Ready = "Ready!"

    class MsgBox:
        Title = "Successfully Downloaded"
        Content = "File Saved At: {}"
        RE_Title = "Runtime Information"

    class WrongPath:
        Title = "Invalid Download Path"
        Content = "Invalid Download Path: ' {} ' \nPlease check and modify it in 'Settings'"

    class Modify:
        Enable = "Enable"
        Disable = "Disable"
        ModifyDesc = "Modify Desc..."

    class ModifyDialog:
        Title = "Modify Description!"
        Ok = "OK"
        Cancel = "Cancel"
