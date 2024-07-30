from fastapi import APIRouter, Depends, Request, Body
from pydantic import BaseModel, Field


router = APIRouter()


@router.get(
    "/youtube",
    tags=['whisper'],
    operation_id="youtube",
    summary="YouTubeの動画を文字起こしする",
)
async def v1_route(video_id: str):
    """
    YouTubeの動画を文字起こしする
    """
    from libs.whisper import youtube_whisper

    return await youtube_whisper(video_id)

