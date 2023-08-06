#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : 异步任务
# @Time         : 2023/5/29 09:58
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *

from fastapi.responses import Response, StreamingResponse, JSONResponse
from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, BackgroundTasks

app = FastAPI()


def task():
    logger.info(f"开始：{time.ctime()}")
    time.sleep(3)
    logger.info(f"结束：{time.ctime()}")


@app.get("/")
async def completions(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)
    logger.info(f"##### 请求: {time.ctime()}")

    return {'a': time.ctime()}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
