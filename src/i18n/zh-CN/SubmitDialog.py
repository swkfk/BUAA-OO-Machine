class Strings:
    class Window:
        Title = "提交代码 - {}"
        Wait = "等待上传"

    class Status:
        Zipping = "归档代码文件夹..."
        Submitting = "上传中..."
        Unzipping = "解压代码文件夹..."
        Compiling = "编译中..."
        Running = "运行中..."
        Done = "完成！"

        Hint = [Submitting, Unzipping,  Compiling, Running, Done]

        CE_Title = "编译错误！"
        RE_Title = "运行时错误"
        RE_Content = "至少有一个测试点运行时异常！ <br />"\
                     "点击测试点序号的标签（例如 <code>#0</code>） <br />" \
                     "查看 <code>RuntimeError</code> 信息。"

    class Ask:
        Title = "请输入 Java 主类，需要包含完整包名"
        Confirm = "确认"
        Cancel = "取消"
        NoAskMore = "确认（不再询问）"
