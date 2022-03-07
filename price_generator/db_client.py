from asyncio import CancelledError
from datetime import datetime
from settings import settings
from pydantic import BaseModel

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class TickerData(BaseModel):
    created_at: datetime
    ticker: str
    price: int


class DBClient:
    def __init__(self):
        self._collection = None

    @property
    def collection(self):
        if self._collection:
            return self._collection

        uri = f"mongodb://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
        client = MongoClient(host=uri)
        db = client.get_database(settings.DB_NAME)
        self._collection = db.get_collection(settings.DB_COLLECTION)

        return self._collection

    async def insert_one(self, ticker: TickerData):
        try:
            result_id = self.collection.insert_one(ticker.dict()).inserted_id
            return result_id
        except ServerSelectionTimeoutError:
            raise CancelledError("Server Connection refused by timeout")
        except Exception as e:
            raise CancelledError(f"Unhandled Exception {e}")
