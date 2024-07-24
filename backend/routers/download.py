from fastapi import APIRouter
from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from core.fs import SOURCE_ROOT, POINT_ROOT, COURSE_ROOT, JsonLoader, GetPointTimestamp, ZipOutputs

router = APIRouter()


@router.get("/src")
async def DownloadSource(digest: str):
    """
    下载源代码
    :param digest: 代码摘要，不检查用户权限
    :return: 源代码压缩包的 FileResponse 对象
    """
    src_file = SOURCE_ROOT / f"{digest}.zip"
    return FileResponse(src_file, filename=f"{digest}.zip")


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
    timestamp = await GetPointTimestamp(proj, unit, point)

    input_file = POINT_ROOT / str(timestamp) / "stdin"
    return FileResponse(input_file, filename=f"Proj{proj}_Unit{unit}_Point{point}_Stdin.txt")


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
    timestamp = await GetPointTimestamp(proj, unit, point)

    output_file = POINT_ROOT / str(timestamp) / "stdout" / user
    return FileResponse(output_file, filename=f"Proj{proj}_Unit{unit}_Point{point}_{user}_Stdout.txt")


@router.get("/all")
async def GetAllOutput(user: str, proj: int, unit: int, point: int):
    """
    下载某个项目、某个单元的全部用户的输出
    :param user: （不使用）
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param point: 测试点的 **编号**，从 0 开始计数
    :return: 全部输出文件压缩包的 FileResponse 对象
    """
    timestamp = await GetPointTimestamp(proj, unit, point)
    output_path = POINT_ROOT / str(timestamp) / "stdout"

    tf = await ZipOutputs(output_path)
    return FileResponse(
        tf.name, filename=f"Proj{proj}_Unit{unit}_Point{point}_Stdout.zip",
        background=BackgroundTask(lambda: tf.close())
    )
