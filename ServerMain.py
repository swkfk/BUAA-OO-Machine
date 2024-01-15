from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn

app = FastAPI(docs_url=None)


@app.get("/index", response_class=HTMLResponse)
def Initial():
    return "<h1>Hello, world!</h1>"


if __name__ == "__main__":
    # 浏览器输入地址：
    # http://localhost:8080/index 可以访问 /index 路由
    uvicorn.run(app, host="0.0.0.0", port=8080)
