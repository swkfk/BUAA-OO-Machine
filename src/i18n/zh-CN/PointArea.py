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
        Others = "保存所有人的 Stdout"

        Dict = {
            "input": Input,
            "output": Output,
            "all": Others
        }

    class Bar:
        Download = "正在下载 ..."
        ReadMsg = "正在请求信息 ..."
        Ready = "就绪！"

    class MsgBox:
        Title = "下载完成"
        Content = "文件保存：{}"
        RE_Title = "测试点运行信息"

    class WrongPath:
        Title = "下载路径错误"
        Content = "非法的下载路径：' {} ' \n请前往 “设置” 检查、修改。"

    class Modify:
        Enable = "启用测试点"
        Disable = "禁用测试点"
        ModifyDesc = "修改描述..."
