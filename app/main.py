from fastapi.middleware.cors import CORSMiddleware
import os
import libs.envloader

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager


# スケジューラー
import asyncio
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

# router
from api.whisper.router import router as v1_whisper_router



API_HOST = os.getenv("API_HOST")


# スケジューラー
scheduler = BackgroundScheduler()


def run_async_task(task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(task())
    loop.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event")
    yield
    print("shutdown event")


app = FastAPI(
    lifespan=lifespan,
    title="microAI API",
    description="""
""",
    servers=[
        {
            "url": API_HOST
        }
    ],
    version="0.0.2",
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://ubot.localhost.jp:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# スケジューラー
# 動画の字幕を取得してDBに保存する
# scheduler.add_job(lambda: run_async_task(taskCaptions),
#                   IntervalTrigger(seconds=5), max_instances=1)
# チャンネルの再生リストの一覧、及び、リストに含まれる動画の一覧を取得し、DBに保存する
# scheduler.add_job(lambda: run_async_task(taskPlayLists),
#                   IntervalTrigger(seconds=5), max_instances=1)
# # 動画のキャプション、または文字起こし結果をDifyのナレッジど同期する
# scheduler.add_job(lambda: run_async_task(taskDocuments),
#                   IntervalTrigger(seconds=5), max_instances=1)
# # ドキュメントのステータス(enable, disable)をあるべき値にしていく
# scheduler.add_job(lambda: run_async_task(taskDocumentsStatus),
#                   IntervalTrigger(seconds=5), max_instances=1)
scheduler.start()


app.include_router(v1_whisper_router, prefix="/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # リクエストデータをログに出力
    body = await request.body()

    print("[ERROR:422]---------------------------------")
    print(body.decode('utf-8'))
    print("[ERROR:422]---------------------------------")

    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )
