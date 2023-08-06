from hamunafs.utils.redisutil import XRedisAsync

import asyncio

redis = XRedisAsync('cache.ai.hamuna.club', '1987yang', 6379)

asyncio.run(redis.zadd('1', '2', 3))