import json
import aioredis
import os
import time


async def saveCache(cache_key: any, data: any):
    """
    キャッシュを保存する
    """
    if not isinstance(cache_key, str):
        cache_key = json.dumps(cache_key)

    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    cache_data = {
        "time": int(time.time()),
        "data": data
    }

    redis = aioredis.from_url(f"redis://{REDIS_URL}", password=REDIS_PASSWORD)
    # 修正: cache_dataをjsonに変換
    await redis.set(cache_key, json.dumps(cache_data), ex=86400*7)
    await redis.close()


async def getCache(cache_key: any, cache_seconds: int = 420):
    """
    キャッシュを取得する
    """
    if not isinstance(cache_key, str):
        cache_key = json.dumps(cache_key)

    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    redis = aioredis.from_url(f"redis://{REDIS_URL}", password=REDIS_PASSWORD)
    cache_data = await redis.get(cache_key)
    await redis.close()

    if cache_data:
        cache_data = json.loads(cache_data)  # 修正: evalからjson.loadsに変更
        if int(time.time()) - cache_data['time'] < cache_seconds:
            return cache_data['data']
    else:
        pass

    return None
