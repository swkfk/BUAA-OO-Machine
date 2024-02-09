class Strings:
    class Widget:
        Index = "#{}"
        Same = "与你一致 {} 人"
        Diff = "存在差异 {} 人"

        @staticmethod
        def ToolTip(lst):
            return "".join((f"<li>{p}</li>" for p in lst))

    class Download:
        Input = "保存 Stdin"
        Output = "保存 Stdout"
        Others = "保存其他人的 Stdout"

        Dict = {
            "input": Input,
            "output": Output,
            "all": Others
        }

    class Bar:
        Download = "正在下载 ..."
        Ready = "就绪！"

    class MsgBox:
        Title = "下载完成"
        Content = "文件保存：{}"
