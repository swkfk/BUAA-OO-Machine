import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
import uvicorn

from core.fs import ensure_directory
from routers.connect import router as router_conn
from routers.query import router as router_query
from routers.submit import router as router_submit
from routers.download import router as router_download
from routers.upload import router as router_upload
from routers.errors import router as router_errors
from routers.upgrade import router as router_upgrade

app = FastAPI(docs_url=None)

app.include_router(router_conn)  # 连接测试
app.include_router(router_query)  # 列举题目内容
app.include_router(router_submit)  # 提交代码
app.include_router(router_download)  # 下载代码、输入、输出
app.include_router(router_upload)  # 上传测试数据
app.include_router(router_errors)  # 错误信息交互
app.include_router(router_upgrade)  # 前端检查更新

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s %(message)s",
            "use_colors": False,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default_file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "uvicorn.default.log",
            "mode": "a",
            "maxBytes": 100 * 1024,
            "backupCount": 3,
        },
        "access_file": {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "uvicorn.access.log",
            "mode": "a",
            "maxBytes": 100 * 1024,
            "backupCount": 3,
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default_file"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access_file"], "level": "INFO", "propagate": False},
    },
}

if __name__ == "__main__":
    ensure_directory()
    uvicorn.run(app, host="0.0.0.0", port=5080, log_config=LOGGING_CONFIG)
