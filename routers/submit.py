import asyncio
import base64
import time
import hashlib
import json
from typing import Optional

from fastapi import APIRouter, UploadFile, File, WebSocket
from starlette.websockets import WebSocketState, WebSocketDisconnect

from core.fs import COURSE_ROOT, JsonLoader, SOURCE_ROOT, USER_ROOT, JAVA_ROOT
from core.judge_core import JudgeCore
from core.submit_cacher import PushSubmitInfo, PopSubmitInfo

router = APIRouter()


@router.post("/submit")
async def SubmitCode(user: str, proj: int, unit: int, class_b64: str,
                     passwd: Optional[str] = None, salt: Optional[str] = None,
                     file: UploadFile = File(...)):
    """
    提交代码，提交文件为压缩包，不包含 "src" 文件夹
    :param user: 用户名，临时用户的用户名为 "__TEMP__"
    :param proj: 项目的 **编号**， 从 0 开始计数
    :param unit: 单元的 **编号**， 从 0 开始计数
    :param class_b64: 主类的 url-safe base64 编码
    :param passwd: 压缩包密码（加密后），与旧版本前端兼容
    :param salt: 压缩包密码加密使用的 salt，与旧版本前端兼容
    :param file: 接收的文件对象
    :return: 该次提交的代码摘要（使用 md5 算法加盐）
    """
    file = await file.read()
    main_class = base64.urlsafe_b64decode(class_b64).decode('utf-8')
    digest = hashlib.md5(file).hexdigest()
    digest = hashlib.md5(f"@{proj}.{unit}#{digest}#BY:{user}#CALL:{main_class}".encode('utf-8')).hexdigest()

    point_user_file = COURSE_ROOT / f"{proj}" / f"{unit}.submit.json"
    if not point_user_file.exists():
        point_user_file.write_text("{}")
    point_user_obj = await JsonLoader(point_user_file)
    point_user_obj[user] = digest
    with open(point_user_file, "w") as f:
        json.dump(point_user_obj, f)

    source_file = SOURCE_ROOT / f"{digest}.zip"
    class_file = SOURCE_ROOT / f"{digest}.entry"
    with open(source_file, "wb") as f:
        f.write(file)
    class_file.write_text(main_class)

    PushSubmitInfo(digest, (digest, (user, proj, unit), (passwd, salt)))

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


@router.websocket("/status/{digest}")
async def CheckSubmitStatus(ws: WebSocket, digest: str):
    """
    发起、查询提交状态
    :param ws: WebSocket 连接
    :param digest: 查询的提交的代码摘要
    :return: 一个表示当前状态的字符串，当且仅当为以下四种（且顺序不可乱）：
        "Submitted" 代码已提交，这是显然成立的
        "Unzipped"  代码已经在服务器端成功解压
        "Compiled"  代码编译成功
        "Done"      全部测评与比对工作已经完成
    """
    await ws.accept()
    JudgeCore(ws, *PopSubmitInfo(digest)).run()
    # Keep the Socket Connection
    try:
        await ws.receive_text()
    except WebSocketDisconnect:
        pass
