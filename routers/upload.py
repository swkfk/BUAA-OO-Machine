import base64
import json
import time

from fastapi import APIRouter, UploadFile, File

from core.fs import COURSE_ROOT, JsonLoader, POINT_ROOT

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
    timestamp = int(time.time() * 1000)
    desc = base64.urlsafe_b64decode(desc).decode('utf-8')

    unit_file = COURSE_ROOT / f"{proj}" / f"{unit}.json"
    point_file = POINT_ROOT / f"{timestamp}" / "stdin"
    unit_obj = await JsonLoader(unit_file)

    unit_obj.append({
        "timestamp": timestamp,
        "desc": desc
    })

    file = await file.read()

    f_json = open(unit_file, "w")
    json.dump(unit_obj, f_json)

    (POINT_ROOT / f"{timestamp}").mkdir(exist_ok=True)
    (POINT_ROOT / f"{timestamp}" / "stdout").mkdir(exist_ok=True)
    f_stdin = open(point_file, "wb")
    f_stdin.write(file)

    f_json.close()
    f_stdin.close()

    return "Success!"
