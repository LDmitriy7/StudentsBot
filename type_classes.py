from dataclasses import dataclass, asdict, field
from pprint import pp
from typing import List


@dataclass
class Profile:
    nickname: str
    phone_number: str
    email: str
    biography: str
    deals_amount: int = 0
    works: list = field(default_factory=list)


@dataclass
class Account:
    _id: int
    page_url: str
    profile: Profile
    balance: int = 0
    subjects: list = field(default_factory=list)


@dataclass
class Bid:
    _id: str
    client_id: int
    worker_id: int
    project_id: str
    text: str


@dataclass
class Chat:
    _id: int
    project_id: str
    chat_type: str
    user_id: int
    link: str
    pair_id: int


@dataclass
class ProjectData:
    work_type: str
    subject: str
    date: str
    description: str
    price: int
    note: str
    files: List[list] = field(default_factory=list)


@dataclass
class Project:
    _id: str
    client_id: int
    data: ProjectData
    client_chat_id: int
    worker_chat_id: int
    status: int = 'Активен'
    post_url: str = None
    worker_id: int = None


@dataclass
class Rating:
    quality: int
    contact: int
    terms: int


@dataclass
class Review:
    _id: str
    client_id: int
    client_name: str
    worker_id: int
    project_id: str
    rating: Rating
    text: str

