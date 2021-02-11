"""Содержит все классы с данными."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from aiogram.utils.helper import Helper, Item
from bson import ObjectId


class DataType(ABC):
    @classmethod
    def from_dict(cls, obj_data: dict):
        # noinspection PyArgumentList
        return cls(**obj_data) if obj_data else None


@dataclass
class Profile(DataType):
    nickname: str
    phone_number: str
    email: str
    biography: str
    deals_amount: int = 0
    works: list = field(default_factory=list)


@dataclass
class Account(DataType):
    balance: int = 0
    subjects: list = field(default_factory=list)
    profile: Profile = None
    page_url: str = None

    @classmethod
    def from_dict(cls, account: dict) -> Optional[Account]:
        if account:
            profile_data = account.pop('profile', None)
            profile = Profile(**profile_data) if profile_data else None
            return cls(**account, profile=profile)
        return None


@dataclass
class Bid(DataType):
    client_id: int
    project_id: str
    worker_id: int = None
    text: str = None


@dataclass
class Chat(DataType):
    project_id: str
    chat_type: str
    user_id: int
    link: str
    pair_id: int
    _id: int = None

    @property
    def id(self):
        return self._id


@dataclass
class PairChats(DataType):
    client_chat: Chat
    worker_chat: Chat


@dataclass
class ProjectData(DataType):
    work_type: str
    subject: str
    date: str
    description: str
    price: int = None
    note: str = None
    files: List[list] = field(default_factory=list)


@dataclass
class Project(DataType):
    data: ProjectData
    client_id: int
    worker_id: int = None
    status: str = 'Активен'
    post_url: str = None
    client_chat_id: int = None
    worker_chat_id: int = None
    _id: ObjectId = None

    @classmethod
    def from_dict(cls, project: dict) -> Optional[Project]:
        if project:
            project_data = ProjectData(**project.pop('data'))
            return cls(**project, data=project_data)
        return None

    @property
    def id(self) -> str:
        return str(self._id)


@dataclass
class Rating(DataType):
    quality: int
    contact: int
    terms: int


@dataclass
class Review(DataType):
    client_id: int
    client_name: str
    worker_id: int
    project_id: str
    rating: Rating
    text: str

    @classmethod
    def from_dict(cls, review: dict) -> Optional[Review]:
        if review:
            rating = Rating(**review.pop('rating'))
            return cls(**review, rating=rating)
        return None


class Prefixes(Helper):
    """Command-prefixes for deep-links and query.data"""
    GET_PROJECT_ = Item()  # для получения проекта
    DEL_PROJECT_ = Item()  # для запроса удаления проекта
    TOTAL_DEL_PROJECT_ = Item()  # для удаления проекта
    PAY_FOR_PROJECT_ = Item()  # для оплаты проекта
    INVITE_PROJECT_ = Item()  # для предложения проекта автором
    OFFER_PROJECT_ = Item()  # для предложения проекта заказчиком
    PICK_PROJECT_ = Item()  # для принятия персонального проекта автором

    GET_FILES_ = Item()  # для получения файлов к проекту

    SEND_BID_ = Item()  # для заявки на проект
    PICK_BID_ = Item()  # для принятия заявки
