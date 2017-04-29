import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGOHOST = os.getenv('MONGOHOST') or 'localhost'
MONGOPORT = int(os.getenv('MONGOPORT') or '27017')

async def setup_db():
    client = AsyncIOMotorClient(MONGOHOST, MONGOPORT)
    dordb = client['dordb']         # 存储寝室电表号
    dorcol = dordb['dormitories']   # 寝室电表号集合
    return dordb
