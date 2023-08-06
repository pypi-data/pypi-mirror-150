import redis
from django.conf import settings

try:
    REDIS_CONFIG = settings.SERGEI['DATA_STORE']['REDIS']['CONNECTION']
except KeyError:
    pass


r = redis.Redis(
    host=REDIS_CONFIG["REDIS_HOST"],
    port=REDIS_CONFIG['REDIS_PORT'],
    password=REDIS_CONFIG['REDIS_PASSWORD'],
    decode_responses=True,
)


def setTokenRedis(TOKEN: str, ex=60000):
    return r.set(TOKEN, TOKEN, ex=ex)


def getTokenRedis(TOKEN: str):
    if r.get(TOKEN) is None:
        return False
    else:
        return True
