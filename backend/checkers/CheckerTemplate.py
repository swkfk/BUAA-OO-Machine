from typing import IO

from checkers.CheckerMetadata import CheckerMetadata

"""
关于 __init__.py 文件
需要提供形如下面的内容：

Checkers = {
    "P1U2": (P1U2.CompareType, P1U2.Fn),
}

其中，键为添加单元时设置的 judge-method，值为一个二元 tuple，含义显见
"""


def _check_main(**kwargs) -> (bool, str):
    fin: IO = kwargs.get("fin")  # Stdin 文件对象
    fout: IO = kwargs.get("fout")  # 该用户的 Stdout 文件对象
    fcmp: IO = kwargs.get("fcmp")  # 待比较的用户的 Stdout 文件对象（如果 CompareType 为 Checker 则取不到这个参数）

    stdin = fin.read()
    ...

    # 如果 CompareType 为 Checker 或 Both，返回的信息将会展示给用户，第一个参数作为正确与否的判断
    if ...:
        return True, "Correct"
    else:
        return False, "Wrong Answer"


CompareType = CheckerMetadata.Checker

# 给测评机调用的
Fn = _check_main
