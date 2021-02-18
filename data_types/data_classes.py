"""Contain all data classes."""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import List, Optional, Union

from bson import ObjectId


@dataclass
class DataType:

    @property
    def id(self) -> Union[str, int, None]:
        if hasattr(self, '_id'):
            if isinstance(self._id, ObjectId):
                return str(self._id)
            return self._id
        raise AttributeError(f'{self.__class__} does not have id field.')

    @id.setter
    def id(self, value: Union[str, int, None]):
        if hasattr(self, '_id'):
            setattr(self, '_id', value)
        else:
            raise AttributeError(f'{self.__class__} does not have id field.')

    @classmethod
    def _resolve_fields(cls, obj_data: dict) -> dict:
        cls_fields = {f.name for f in fields(cls)}
        resolved_data = {}
        for key, value in obj_data.items():
            if key in cls_fields:
                resolved_data[key] = value
        return resolved_data

    @classmethod
    def from_dict(cls, obj_data: dict):
        """Exclude extra items, return instance if data provided else None."""
        if cls is DataType:
            err_text = f'This method is only for {cls.__name__} subclasses'
            raise AttributeError(err_text)

        if obj_data:
            obj_data = cls._resolve_fields(obj_data)
            # noinspection PyArgumentList
            return cls(**obj_data)
        return None


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
    _id: int = None

    @classmethod
    def from_dict(cls, account: dict) -> Optional[Account]:
        if account:
            obj_data = cls._resolve_fields(account)
            profile_data = obj_data.pop('profile', None)
            profile = Profile.from_dict(profile_data)
            return cls(**obj_data, profile=profile)
        return None


@dataclass
class Bid(DataType):
    client_id: int
    project_id: str
    worker_id: int = None
    text: str = None
    _id: ObjectId = None


@dataclass
class Chat(DataType):
    project_id: str
    user_role: str
    user_id: int
    link: str
    pair_id: int
    _id: int = None


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
    status: str
    client_id: int
    worker_id: int = None
    post_url: str = None
    client_chat_id: int = None
    worker_chat_id: int = None
    _id: ObjectId = None

    @classmethod
    def from_dict(cls, project: dict) -> Optional[Project]:
        if project:
            obj_data = cls._resolve_fields(project)
            project_data = obj_data.pop('data', None)
            project_data = ProjectData.from_dict(project_data)
            return cls(**obj_data, data=project_data)
        return None


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
    _id: ObjectId = None

    @classmethod
    def from_dict(cls, review: dict) -> Optional[Review]:
        if review:
            obj_data = cls._resolve_fields(review)
            rating_data = obj_data.pop('rating', None)
            rating = Rating.from_dict(rating_data)
            return cls(**obj_data, rating=rating)
        return None
