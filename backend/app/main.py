import os
import sys

import uvicorn

from fastapi import FastAPI

from controllers import router
from middlewares import corsMiddlewares, staticMiddlewares

if not os.path.exists("static"):
    os.makedirs("static")

app = FastAPI()

app.include_router(router.router)

corsMiddlewares.add(app)
staticMiddlewares.add(app)

@app.get("/")
def root():
    return {"hello world": "xin chào"}

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)