import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGOHOST = os.getenv('MONGOHOST') or 'localhost'
MONGOPORT = int(os.getenv('MONGOPORT') or '27017')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME') or "muxi"
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD') or "nopassword"

async def setup_db():
    # client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    mongo_uri = "mongodb://{}:{}@{}:{}".format(MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_PORT)
    client = AsyncIOMotorClient(mongo_uri)    
    dordb = client['dordb']         # 存储寝室电表号
    dorcol = dordb['dormitories']   # 寝室电表号集合
    return dordb
