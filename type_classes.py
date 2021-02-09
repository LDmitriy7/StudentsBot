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
    # _id: int
    balance: int = 0
    subjects: list = field(default_factory=list)
    profile: Profile = None
    page_url: str = None


@dataclass
class Bid:
    client_id: int
    project_id: str
    worker_id: int = None
    text: str = None


@dataclass
class Chat:
    # _id: int
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
    status: str
    data: ProjectData
    client_id: int
    worker_id: int = None
    post_url: str = None
    client_chat_id: int = None
    worker_chat_id: int = None


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
