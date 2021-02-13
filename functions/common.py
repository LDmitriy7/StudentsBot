from dataclasses import asdict, fields
from typing import List, Optional

import datatypes
from config import START_LINK
from datatypes import Prefixes
from loader import users_db

__all__ = ['count_avg_rating', 'get_invite_project_url', 'get_chat_link', 'get_all_nicknames']


async def get_chat_link(chat_id: int) -> Optional[str]:
    """Return chat link if chat exists."""
    chat = await users_db.get_chat_by_id(chat_id)
    return chat.link if chat else None


def get_invite_project_url(user_id: int) -> str:
    """Создает ссылку-приглашение в личный проект."""
    payload = f'{Prefixes.INVITE_PROJECT_}{user_id}'
    return START_LINK.format(payload)


def count_avg_rating(reviews: List[datatypes.Review]) -> dict:
    """Count average user's rating dict from reviews."""
    avg_rating = {field.name: 0 for field in fields(datatypes.Rating)}
    for review in reviews:
        rating_dict = asdict(review.rating)
        for rate, amount in rating_dict.items():
            avg_rating[rate] += amount

    reviews_amount = len(reviews) or 1
    for rate, amount in avg_rating.items():
        avg_rating[rate] /= reviews_amount

    return avg_rating


async def get_all_nicknames() -> set:
    """Возращает набор всех никнеймов в коллекции аккаунтов."""
    nicknames = set()
    for a in await users_db.get_all_accounts():
        if a.profile:
            nicknames.add(a.profile.nickname)
    return nicknames
