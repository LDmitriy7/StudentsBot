from dataclasses import dataclass, field
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
    client_id: int
    worker_id: int
    project_id: str
    text: str
    # _id: str = None


@dataclass
class Chat:
    _id: int
    project_id: str
    chat_type: str
    user_id: int
    link: str
    pair_id: int


@dataclass
class PairChats:
    client_chat: Chat
    worker_chat: Chat


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
    client_id: int
    data: ProjectData
    status: str
    client_chat_id: int = None
    worker_chat_id: int = None
    post_url: str = None
    worker_id: int = None
    # _id: str = None


@dataclass
class Rating:
    quality: int
    contact: int
    terms: int


@dataclass
class Review:
    client_id: int
    client_name: str
    worker_id: int
    project_id: str
    rating: Rating
    text: str
    # _id: str = None
