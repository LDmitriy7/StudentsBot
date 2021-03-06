"""Contain all data models."""
from __future__ import annotations

from dataclasses import dataclass, field, fields, asdict, Field
from typing import List, Union

from bson import ObjectId


@dataclass
class DataModel:

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

    def to_dict(self):
        return asdict(self)

    @classmethod
    def field_names(cls) -> list[str]:
        return [f.name for f in fields(cls)]

    @classmethod
    def fields(cls) -> list[Field]:
        return fields(cls)

    @classmethod
    def _resolve_fields(cls, obj_data: dict) -> dict:
        cls_fields = {f.name for f in cls.fields()}
        resolved_data = {}
        for key, value in obj_data.items():
            if key in cls_fields:
                resolved_data[key] = value
        return resolved_data

    @classmethod
    def from_dict(cls, obj_data: dict):
        resolved_data = cls._resolve_fields(obj_data)

        for _field, value in resolved_data.items():
            field_type_name = cls.__annotations__.get(_field)
            if field_type_name:
                field_type = eval(field_type_name)
                factory = getattr(field_type, 'from_dict', None)
                if factory:
                    resolved_data[_field] = factory(value)

        # noinspection PyArgumentList
        return cls(**resolved_data)


@dataclass
class Profile(DataModel):
    nickname: str
    phone_number: str
    email: str
    biography: str
    deals_amount: int = 0
    works: list = field(default_factory=list)


@dataclass
class Account(DataModel):
    balance: int = 0
    subjects: list = field(default_factory=list)
    profile: Profile = None
    page_url: str = None
    _id: int = None


@dataclass
class Bid(DataModel):
    client_id: int
    project_id: str
    worker_id: int = None
    text: str = None
    _id: ObjectId = None


@dataclass
class Chat(DataModel):
    project_id: str
    user_role: str
    user_id: int
    link: str
    pair_id: int
    _id: int = None


@dataclass
class PairChats(DataModel):
    client_chat: Chat
    worker_chat: Chat


@dataclass
class ProjectData(DataModel):
    work_type: str
    subject: str
    date: str
    description: str
    price: int = None
    note: str = None
    files: List[list] = field(default_factory=list)


@dataclass
class Project(DataModel):
    data: ProjectData
    status: str
    client_id: int
    worker_id: int = None
    post_url: str = None
    client_chat_id: int = None
    worker_chat_id: int = None
    _id: ObjectId = None


@dataclass
class Rating(DataModel):
    quality: int
    contact: int
    terms: int


@dataclass
class Review(DataModel):
    client_id: int
    client_name: str
    worker_id: int
    project_id: str
    subject: str
    rating: Rating
    text: str
    _id: ObjectId = None
