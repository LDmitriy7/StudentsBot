"""Класс для асинхронной работы с MongoDB"""

from typing import List, Optional, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.results import InsertOneResult
from type_classes import Chat, ProjectData, Project, Bid, Review, Profile, Rating, Account
from dataclasses import asdict

ACCOUNTS = 'accounts'
PROJECTS = 'projects'
BIDS = 'bids'
CHATS = 'chats'
REVIEWS = 'reviews'
WITHDRAWALS = 'withdrawals'

PROJECTS_INDEX = (PROJECTS, ['client_id', 'worker_id', 'data.subject'])  # 3 indexes for PROJECTS
BIDS_INDEX = (BIDS, ['client_id', 'worker_id'])
INDEXES = [PROJECTS_INDEX, BIDS_INDEX]


class MongoClient:
    """Содержит базовые методы для взаимодействия с базой."""

    def __init__(self, host='localhost', port=27017, db_name='users', index=True):
        self._host = host
        self._port = port
        self._db_name = db_name
        self._index = index

        self._mongo: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def _get_client(self) -> AsyncIOMotorClient:
        if isinstance(self._mongo, AsyncIOMotorClient):
            return self._mongo

        uri = f'mongodb://{self._host}:{self._port}'
        self._mongo = AsyncIOMotorClient(uri)
        return self._mongo

    async def get_db(self) -> AsyncIOMotorDatabase:
        if isinstance(self._db, AsyncIOMotorDatabase):
            return self._db

        mongo = await self._get_client()
        self._db = mongo.get_database(self._db_name)

        if self._index:
            await self.apply_index(self._db)
        return self._db

    @staticmethod
    async def apply_index(db):
        for index in INDEXES:
            collection, keys = index
            for key in keys:
                await db[collection].create_index(keys=[(key, 1)], background=True)

    async def close(self):
        if self._mongo:
            self._mongo.close()


class MongoAdder(MongoClient):
    """Содержит методы для добавления объектов в базу."""

    async def _add_object(self, collection, **kwargs) -> str:
        db = await self.get_db()
        object_data = dict(**kwargs)
        result: InsertOneResult = await db[collection].insert_one(object_data)
        return str(result.inserted_id)

    async def add_project(self, client_id: int, project_data: dict) -> str:
        worker_id = project_data.pop('worker_id', None)
        post_url = project_data.pop('post_url', None)
        status = project_data.pop('status', 'Активен')

        inserted_id = await self._add_object(
            PROJECTS,
            client_id=client_id,
            worker_id=worker_id,
            status=status,
            post_url=post_url,
            data=project_data,
        )
        return inserted_id

    async def add_project_test(self, project: Project):
        return await self._add_object(PROJECTS, **asdict(project))

    async def add_bid(self, client_id: int, project_id: str, worker_id: int, text: str) -> str:
        inserted_id = await self._add_object(
            BIDS,
            client_id=client_id,
            worker_id=worker_id,
            project_id=project_id,
            text=text,
        )
        return inserted_id

    async def add_bid_test(self, bid: Bid) -> str:
        return await self._add_object(BIDS, **asdict(bid))

    async def add_chat(self, project_id: str, chat_id: int, chat_type: str, user_id: int, link: str,
                       pair_id: int) -> str:
        inserted_id = await self._add_object(
            CHATS,
            _id=chat_id,
            project_id=project_id,
            chat_type=chat_type,
            user_id=user_id,
            link=link,
            pair_id=pair_id,
        )
        return inserted_id

    async def add_chat_test(self, chat: Chat):
        return await self._add_object(CHATS, **asdict(chat))

    async def add_review(self, client_id: int, client_name: str, worker_id: int, project_id: str, rating: dict,
                         text: str) -> str:
        inserted_id = await self._add_object(
            REVIEWS,
            client_id=client_id,
            client_name=client_name,
            worker_id=worker_id,
            project_id=project_id,
            rating=rating,
            text=text
        )
        return inserted_id


class MongoGetter(MongoClient):
    """Содержит методы для поиска объектов в базе."""

    async def _get_object(self, collection: str, _filter: dict, many=False) -> Union[dict, List[dict]]:
        db = await self.get_db()
        if many:
            result = [p async for p in db[collection].find(_filter)]
        else:
            result = await db[collection].find_one(_filter)
        return result

    async def get_all_accounts(self) -> List[dict]:
        return await self._get_object(ACCOUNTS, {}, many=True)

    async def get_all_projects(self) -> List[dict]:
        return await self._get_object(PROJECTS, {}, many=True)

    async def get_project_by_id(self, project_id: str) -> dict:
        oid = ObjectId(project_id)
        project = await self._get_object(PROJECTS, {'_id': oid})
        return project

    async def get_projects_by_user(self, client_id: int = None, worker_id: int = None) -> List[dict]:
        if client_id:
            _filter = {'client_id': client_id}
        elif worker_id:
            _filter = {'worker_id': worker_id}
        else:
            raise ValueError('Must specify one of values.')

        projects = await self._get_object(PROJECTS, _filter, many=True)
        return projects

    async def get_projects_by_subjects(self, subjects: List[str], only_active=True) -> List[dict]:
        _filter = {'data.subject': {'$in': subjects}}
        if only_active:
            _filter.update(status='Активен')
        projects = await self._get_object(PROJECTS, _filter, many=True)
        return projects

    async def get_account_by_id(self, user_id: int) -> dict:
        _filter = {'_id': user_id}
        account = await self._get_object(ACCOUNTS, _filter)
        return account

    async def get_chat_by_id(self, chat_id: int) -> dict:
        _filter = {'_id': chat_id}
        chat = await self._get_object(CHATS, _filter)
        return chat

    async def get_bid_by_id(self, bid_id: str) -> dict:
        oid = ObjectId(bid_id)
        bid = await self._get_object(BIDS, {'_id': oid})
        return bid

    async def get_reviews_by_worker(self, worker_id: int) -> List[dict]:
        return await self._get_object(REVIEWS, {'worker_id': worker_id}, many=True)


class MongoDeleter(MongoClient):
    """Содержит методы для удаления объектов из базы."""

    async def _delete_object(self, collection: str, _filter: dict):
        db = await self.get_db()
        await db[collection].delete_one(_filter)

    async def delete_project_by_id(self, project_id: str):
        oid = ObjectId(project_id)
        await self._delete_object(PROJECTS, {'_id': oid})

    async def delete_account_by_id(self, user_id: int):
        await self._delete_object(ACCOUNTS, {'_id': user_id})

    async def delete_bid_by_id(self, bid_id: str):
        oid = ObjectId(bid_id)
        await self._delete_object(BIDS, {'_id': oid})

    async def delete_chat_by_id(self, chat_id: int):
        await self._delete_object(CHATS, {'_id': chat_id})


class MongoUpdater(MongoClient):
    """Содержит методы для обновления объектов в базе."""

    async def _update_object(self, collection: str, _filter: dict, operator: str, update: dict, upsert=True):
        db = await self.get_db()
        await db[collection].update_one(_filter, {operator: update}, upsert)

    async def incr_balance(self, user_id: int, amount: int):
        await self._update_object(ACCOUNTS, {'_id': user_id}, '$inc', {'balance': amount})

    async def update_project_status(self, project_id: str, new_status: str):
        oid = ObjectId(project_id)
        await self._update_object(PROJECTS, {'_id': oid}, '$set', {'status': new_status}, upsert=False)

    async def update_account_subjects(self, user_id: int, subjects: List[str]):
        await self._update_object(
            ACCOUNTS, {'_id': user_id}, '$set',
            {'subjects': subjects},
        )

    async def update_account_profile(self, user_id: int, profile_data: dict):
        await self._update_object(ACCOUNTS, {'_id': user_id}, '$set', {'profile': profile_data})

    async def update_account_page_url(self, user_id: int, page_url: str):
        await self._update_object(ACCOUNTS, {'_id': user_id}, '$set', {'page_url': page_url}, upsert=False)


class MongoProfileUpdater(MongoUpdater):
    """Содержит методы для обновления профиля аккаунта."""

    async def _update_profile(self, user_id: int, field: str, value):
        await self._update_object(ACCOUNTS, {'_id': user_id}, '$set', {f'profile.{field}': value})

    async def update_profile_nickname(self, user_id: int, nickname: str):
        await self._update_profile(user_id, 'nickname', nickname)

    async def update_profile_phone_number(self, user_id: int, phone_number: str):
        await self._update_profile(user_id, 'phone_number', phone_number)

    async def update_profile_email(self, user_id: int, email: str):
        await self._update_profile(user_id, 'email', email)

    async def update_profile_biography(self, user_id: int, biography: str):
        await self._update_profile(user_id, 'biography', biography)

    async def update_profile_works(self, user_id: int, works: List[str]):
        await self._update_profile(user_id, 'works', works)


class MongoDB(MongoAdder, MongoGetter, MongoDeleter, MongoProfileUpdater):
    """Наследует все наборы методов управления базой."""


if __name__ == '__main__':
    import asyncio

    db = MongoDB()
    func = db.add_review(123, 321, '7test7', {'quality': 4, 'contact': 5, 'terms': 4}, 'Спасибо!')
    func2 = db.get_reviews_by_worker(321)
    r = asyncio.run(func2)
    print(r)
