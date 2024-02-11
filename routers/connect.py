from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def ConnectTest():
    """
    测试连接，前端的 设置 界面中需要使用
    :return: 一个内容为 "Success!" 的字符串
    """
    return "Success!"
