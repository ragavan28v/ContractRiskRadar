from motor.motor_asyncio import AsyncIOMotorClient

from .config import get_settings

settings = get_settings()

# connect to Mongo; URI may or may not include a database name
client = AsyncIOMotorClient(settings.MONGO_URI)

# determine default database name
from urllib.parse import urlparse
parsed = urlparse(settings.MONGO_URI)
# path component starts with '/dbname'
db_name = parsed.path[1:] if parsed.path and parsed.path != "/" else "contractRadar"

# motor's get_default_database() fails if URI has no db, so fall back
try:
    db = client.get_default_database()
except Exception:
    db = client[db_name]

# collection for storing contract documents
contracts_collection = db["contracts"]
