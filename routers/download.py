from fastapi import APIRouter

router = APIRouter()


@router.get("/src")
async def DownloadSource(digest: str):
    """
    下载源代码
    :param digest: 代码摘要，不检查用户权限
    :return: 源代码压缩包的 FileResponse 对象
    """
    pass


@router.get("/input")
async def GetInput(user: str, proj: int, unit: int, point: int):
    """
    下载某个项目、某个单元的某一个测试点的输入
    :param user: （不使用）
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param point: 测试点的 **编号**，从 0 开始计数
    :return: 输入文件的 FileResponse 对象
    """
    pass


@router.get("/output")
async def GetOutput(user: str, proj: int, unit: int, point: int):
    """
    下载指定用户某个项目、某个单元的某一个测试点的输出
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param point: 测试点的 **编号**，从 0 开始计数
    :return: 输出文件的 FileResponse 对象
    """
    pass


@router.get("/output")
async def GetAllOutput(user: str, proj: int, unit: int, point: int):
    """
    下载某个项目、某个单元的全部用户的输出
    :param user: （不使用）
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param point: 测试点的 **编号**，从 0 开始计数
    :return: 全部输出文件压缩包的 FileResponse 对象
    """
    pass
