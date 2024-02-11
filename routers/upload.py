from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/upload")
async def UploadTestPoint(proj: int, unit: int, desc: str, file: UploadFile = File(...)):
    """
    上传一个测试的输入数据，文件方式提交
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param desc: 测试点描述（url-safe 的 base64 编码）
    :param file: 接收的文件对象
    :return: 若成功，则为字符串 "Success!"，否则可以包含失败信息
    """
    pass
