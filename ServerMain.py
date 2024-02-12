from fastapi import FastAPI
import uvicorn

from core.fs import ensure_directory
from routers.connect import router as router_conn
from routers.query import router as router_query
from routers.submit import router as router_submit
from routers.download import router as router_download
from routers.upload import router as router_upload

app = FastAPI(docs_url=None)

app.include_router(router_conn)  # 连接测试
app.include_router(router_query)  # 列举题目内容
app.include_router(router_submit)  # 提交代码
app.include_router(router_download)  # 下载代码、输入、输出
app.include_router(router_upload)  # 上传测试数据

if __name__ == "__main__":
    ensure_directory()
    uvicorn.run(app, host="0.0.0.0", port=8080)
