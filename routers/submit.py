import time
import hashlib
import json

from fastapi import APIRouter, UploadFile, File

from core.fs import COURSE_ROOT, JsonLoader, SOURCE_ROOT, USER_ROOT

router = APIRouter()


@router.post("/submit")
async def SubmitCode(user: str, proj: int, unit: int, file: UploadFile = File(...)):
    """
    提交代码，提交文件为压缩包，不包含 "src" 文件夹
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param file: 接收的文件对象
    :return: 该次提交的代码摘要（使用 md5 算法）
    """
    file = await file.read()
    digest = hashlib.md5(file).hexdigest()

    point_user_file = COURSE_ROOT / f"{proj}" / f"{unit}.submit.json"
    if not point_user_file.exists():
        point_user_file.write_text("{}")
    point_user_obj = await JsonLoader(point_user_file)
    point_user_obj[user] = digest
    with open(point_user_file, "w") as f:
        json.dump(point_user_obj, f)

    source_file = SOURCE_ROOT / f"{digest}.zip"
    with open(source_file, "wb") as f:
        f.write(file)

    user_file = USER_ROOT / f"{user}.json"
    if not user_file.exists():
        user_file.write_text("[]")
    user_obj = await JsonLoader(user_file)
    user_obj.append({
        "digest": digest,
        "time": time.strftime('%Y-%m-%d %H:%M', time.localtime())
    })
    with open(user_file, "w") as f:
        json.dump(user_obj, f)

    return digest


@router.get("/status")
async def CheckSubmitStatus(digest: str):
    """
    轮询提交状态的接口
    :param digest: 查询的提交的代码摘要
    :return: 一个表示当前状态的字符串，当且仅当为以下四种（且顺序不可乱）：
        "Submitted" 代码已提交，这是显然成立的
        "Unzipped"  代码已经在服务器端成功解压
        "Compiled"  代码编译成功
        "Done"      全部测评与比对工作已经完成
    """
    return "Done"
