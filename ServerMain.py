from fastapi import FastAPI
import uvicorn

from routers.connection import router as router_conn

app = FastAPI(docs_url=None)

app.include_router(router_conn)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
