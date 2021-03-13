"""Contain all data models."""
from dataclasses import dataclass, field

from data_types._models import DataModel, MongoModel


@dataclass
class Profile(DataModel):
    nickname: str
    phone_number: str
    email: str
    biography: str
    deals_amount: int = 0
    works: list = field(default_factory=list)


@dataclass
class Account(MongoModel):
    balance: int = 0
    subjects: list = field(default_factory=list)
    profile: Profile = None
    page_url: str = None
    _id: int = None


@dataclass
class Bid(MongoModel):
    client_id: int
    project_id: str
    worker_id: int = None
    text: str = None


@dataclass
class Chat(MongoModel):
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
    files: list[list] = field(default_factory=list)


@dataclass
class Project(MongoModel):
    data: ProjectData
    status: str
    client_id: int
    worker_id: int = None
    post_url: str = None
    client_chat_id: int = None
    worker_chat_id: int = None


@dataclass
class Rating(DataModel):
    quality: int
    contact: int
    terms: int


@dataclass
class Review(MongoModel):
    client_id: int
    client_name: str
    worker_id: int
    project_id: str
    subject: str
    rating: Rating
    text: str


@dataclass
class Withdrawal(MongoModel):
    user_id: int
    amount: int
