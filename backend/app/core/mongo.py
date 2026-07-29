from datetime import datetime
from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from .config import get_settings

settings = get_settings()

client = AsyncIOMotorClient(settings.MONGO_URI)

parsed = urlparse(settings.MONGO_URI)
database_name = settings.MONGO_DB_NAME or (
    parsed.path[1:] if parsed.path and parsed.path != "/" else "contract_radar"
)

db = client[database_name]

users_collection = db["users"]
contracts_collection = db["contracts"]
counters_collection = db["counters"]


async def init_mongo_indexes() -> None:
    await users_collection.create_index("email", unique=True)
    await contracts_collection.create_index([("owner_id", 1), ("created_at", -1)])
    await contracts_collection.create_index([("owner_id", 1), ("consent_store", 1), ("created_at", -1)])
    await contracts_collection.create_index([("clauses.id", 1)])


async def next_sequence(name: str) -> int:
    doc = await counters_collection.find_one_and_update(
        {"_id": name},
        {
            "$inc": {"seq": 1},
            "$setOnInsert": {"created_at": datetime.utcnow()},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(doc["seq"])
