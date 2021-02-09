"""Класс для асинхронной работы с MongoDB"""

from dataclasses import asdict
from typing import List, Optional, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.results import InsertOneResult

import type_classes as datatypes

ACCOUNTS = 'accounts'
PROJECTS = 'projects'
BIDS = 'bids'
CHATS = 'chats'
REVIEWS = 'reviews'
WITHDRAWALS = 'withdrawals'

PROJECTS_INDEX = (PROJECTS, ['client_id', 'worker_id', 'data.subject'])
BIDS_INDEX = (BIDS, ['client_id', 'worker_id'])

INDEXES = [PROJECTS_INDEX, BIDS_INDEX]


class MongoClient:
    """Содержит методы управления MongoDB клиентом."""

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
            collection, fields = index
            for field in fields:
                await db[collection].create_index(keys=[(field, 1)], background=True)

    async def close(self):
        if self._mongo:
            self._mongo.close()


class MongoBase(MongoClient):
    """Содержит базовые методы для взаимодействия с базой данных."""

    async def add_object(self, collection: str, object_data: dict, _id=None) -> str:
        """Добавляет объект в коллекцию, возращает его _id."""
        db = await self.get_db()
        if _id:
            object_data['_id'] = _id
        result: InsertOneResult = await db[collection].insert_one(object_data)
        return str(result.inserted_id)

    async def get_object(self, collection: str, _filter: dict, many=False,
                         pop_id=True) -> Union[dict, List[dict], None]:
        """Возвращает из коллекции объект, список объектов [many=True] или None."""
        db = await self.get_db()
        if many:
            result = []
            async for obj in db[collection].find(_filter):
                if pop_id:
                    obj.pop('_id')
                result.append(obj)
        else:
            result = await db[collection].find_one(_filter)
            result.pop('_id')
        return result

    async def delete_object(self, collection: str, _filter: dict):
        """Удаляет объект из коллекции."""
        db = await self.get_db()
        await db[collection].delete_one(_filter)

    async def update_object(self, collection: str, _filter: dict, operator: str, update: dict, upsert=True):
        """Обновляет элемент коллекции, может создать новый элемент при [upsert=True]."""
        db = await self.get_db()
        await db[collection].update_one(_filter, {operator: update}, upsert)


class MongoAdder(MongoBase):
    """Содержит методы для добавления объектов в коллекции."""

    async def add_project(self, project: datatypes.Project) -> str:
        return await self.add_object(PROJECTS, asdict(project))

    async def add_bid(self, bid: datatypes.Bid) -> str:
        return await self.add_object(BIDS, asdict(bid))

    async def add_chat(self, chat_id: int, chat: datatypes.Chat) -> str:
        return await self.add_object(CHATS, asdict(chat), _id=chat_id)

    async def add_review(self, review: datatypes.Review) -> str:
        return await self.add_object(REVIEWS, asdict(review))


class MongoGetter(MongoBase):
    """Содержит методы для поиска объектов в базе."""

    async def get_all_accounts(self) -> List[datatypes.Account]:
        accounts = []
        for a in await self.get_object(ACCOUNTS, {}, many=True):
            profile_data = a.pop('profile', None)
            profile = datatypes.Profile(**profile_data) if profile_data else None
            accounts.append(datatypes.Account(**a, profile=profile))
        return accounts

    async def get_all_projects(self) -> List[dict]:
        return await self._get_object(PROJECTS, {}, many=True)

    async def get_project_by_id(self, project_id: str) -> dict:
        oid = ObjectId(project_id)
        project = await self._get_object(PROJECTS, {'_id': oid})
        return project

    async def get_project_by_id_test(self, project_id: str) -> datatypes.Project:
        oid = ObjectId(project_id)
        project = await self.get_object(PROJECTS, {'_id': oid})
        project.pop('_id')
        project_data = datatypes.ProjectData(**project.pop('data'))
        return datatypes.Project(**project, data=project_data)

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

    async def get_account_by_id_test(self, user_id: int) -> Optional[datatypes.Account]:
        _filter = {'_id': user_id}
        account = await self._get_object(ACCOUNTS, _filter)
        if account:
            profile = account.pop('profile', None)
            profile = datatypes.Profile(**profile) if profile else None
            return datatypes.Account(**account, profile=profile)
        else:
            return None

    async def get_chat_by_id(self, chat_id: int) -> dict:
        _filter = {'_id': chat_id}
        chat = await self._get_object(CHATS, _filter)
        return chat

    async def get_bid_by_id(self, bid_id: str) -> dict:
        oid = ObjectId(bid_id)
        bid = await self._get_object(BIDS, {'_id': oid})
        return bid

    async def get_bid_by_id_test(self, bid_id: str) -> datatypes.Bid:
        oid = ObjectId(bid_id)
        bid = await self.get_object(BIDS, {'_id': oid})
        bid.pop('_id')
        return datatypes.Bid(**bid)

    async def get_reviews_by_worker(self, worker_id: int) -> List[dict]:
        return await self._get_object(REVIEWS, {'worker_id': worker_id}, many=True)


class MongoDeleter(MongoClient):
    """Содержит методы для удаления объектов из базы."""

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
