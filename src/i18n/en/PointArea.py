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
        Ready = "Ready!"

    class MsgBox:
        Title = "Successfully Downloaded"
        Content = "File Saved At: {}"
