"""Класс для асинхронной работы с MongoDB"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Optional
from pymongo.results import InsertOneResult
from bson import ObjectId

ACCOUNTS = 'accounts'
PROJECTS = 'projects'
BIDS = 'bids'


class MongoClient:
    def __init__(self, host='localhost', port=27017, db_name='users'):
        self._host = host
        self._port = port
        self._db_name = db_name

        self._mongo: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def get_client(self) -> AsyncIOMotorClient:
        if isinstance(self._mongo, AsyncIOMotorClient):
            return self._mongo

        uri = f'mongodb://{self._host}:{self._port}'
        self._mongo = AsyncIOMotorClient(uri)
        return self._mongo

    async def get_db(self) -> AsyncIOMotorDatabase:
        if isinstance(self._db, AsyncIOMotorDatabase):
            return self._db

        mongo = await self.get_client()
        self._db = mongo.get_database(self._db_name)

        # if self._index:
        #     await self.apply_index()
        return self._db

    # async def apply_index(self):
    #     db = self._db
    #     for collection in COLLECTIONS:
    #         keys = [('user_id', 1)]
    #         await db[collection].create_index(keys=keys, unique=True, background=True)

    async def close(self):
        if self._mongo:
            self._mongo.close()


class MongoDB(MongoClient):
    """Содержит непосредственно АПИ."""

    async def add_project(self, user_id: int, project_data: dict) -> str:
        db = await self.get_db()
        worker = project_data.pop('worker', None)
        post_url = project_data.pop('post_url', None)

        result: InsertOneResult = await db[PROJECTS].insert_one({
            'user_id': user_id,
            'worker': worker,
            'post_url': post_url,
            'data': project_data
        })

        return str(result.inserted_id)

    async def add_bid(self, user_id: int, worker_id: int, project_id: str, text: str) -> str:
        db = await self.get_db()
        result = await db[BIDS].insert_one(
            {'user_id': user_id,
             'worker': worker_id,
             'project_id': project_id,
             'text': text
             })
        result: InsertOneResult
        return str(result.inserted_id)

    async def get_project_by_id(self, project_id: str) -> dict:
        db = await self.get_db()
        oid = ObjectId(project_id)
        project = await db[PROJECTS].find_one({'_id': oid})
        return project
