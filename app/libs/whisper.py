from faster_whisper import WhisperModel
from libs.cache import getCache, saveCache
import torch
import subprocess

from libs.cache import getCache, saveCache


async def youtube_whisper(video_id: str):
    """
    YouTubeの動画を文字起こしする
    """
    try:

        cache_key = f"youtube_whisper_{video_id}"
        cache_data = await getCache(cache_key)
        if cache_data:
            return cache_data

        video_file_path = await downloadAudio(video_id=video_id)
        model_size = "large-v3"
        MODE = "GPU" if torch.cuda.is_available() else "CPU"

        # Run on GPU with FP16
        if MODE == "GPU":
            model = WhisperModel(model_size, device="cuda", compute_type="float16")
        else:
            model = WhisperModel(model_size, device="cpu", compute_type="int8")

        segments, info = model.transcribe(
            video_file_path, beam_size=5, language='ja')

        print("Detected language '%s' with probability %f" %
            (info.language, info.language_probability))

        texts = []

        for segment in segments:
            texts.append(segment.text)
            print("[%.2fs -> %.2fs] %s" %
                (segment.start, segment.end, segment.text))

        texts = await removeConsecutiveDuplicates(texts)
        texts = "\n".join(texts)
        await saveCache(cache_key, texts)
        return texts
    except Exception as e:
        raise Exception(f"youtube_whisper Error: {str(e)}")


async def removeConsecutiveDuplicates(texts):
    if not texts:
        return texts  # リストが空の場合はそのまま返す

    result = [texts[0]]  # 最初の要素を追加
    for i in range(1, len(texts)):
        if texts[i] != texts[i - 1]:
            result.append(texts[i])
    return result

async def downloadAudio(video_id: str):

    try:

        from pytubefix import YouTube
        link = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()

        output_path = "/tmp/"
        video_file_path = audio_stream.download(
            output_path=output_path, filename=f"{video_id}.mp4", skip_existing=True)
        return video_file_path

    except Exception as e:
        raise Exception(f"downloadAudio Error: {str(e)}")



