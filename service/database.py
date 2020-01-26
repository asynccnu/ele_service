import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://username:secret@localhost:27017/?authSource=admin"

async def setup_db():
    # client = AsyncIOMotorClient(MONGODB_HOST, MONGODB_PORT)
    mongo_uri = MONGO_URI
    client = AsyncIOMotorClient(mongo_uri)    
    dordb = client['dordb']         # 存储寝室电表号
    dorcol = dordb['dormitories']   # 寝室电表号集合
    return dordb
