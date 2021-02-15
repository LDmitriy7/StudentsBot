from dataclasses import asdict, fields
from typing import List, Optional

from aiogram import types

import datatypes
from config import MAIN_CHANNEL, MAIN_POST_URL, START_LINK
from datatypes import Prefixes, Update
from keyboards import inline_funcs
from loader import bot, users_db
from texts import templates

__all__ = ['count_avg_rating', 'get_invite_project_url', 'get_chat_link', 'get_all_nicknames',
           'send_post', 'update_post', 'delete_post', 'get_chat_of_update']


def get_chat_of_update(update: Update) -> types.Chat:
    """Return chat of update (Message or CallbackQuery)."""
    return update.chat if isinstance(update, types.Message) else update.message.chat


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


# posts


async def send_post(
        project_id: str, project_status: str, post_data: datatypes.ProjectData
) -> str:
    """Send post to channel. Return post_url."""
    text = templates.form_post_text(project_status, post_data)
    has_files = bool(post_data.files)
    keyboard = inline_funcs.for_project(project_id, pick_btn=True, files_btn=has_files)

    post_obj = await bot.send_message(MAIN_CHANNEL, text, reply_markup=keyboard)
    post_url = MAIN_POST_URL.format(post_obj.message_id)
    return post_url


async def update_post(project_id: str, project_status: str, post_url: Optional[str], post_data: datatypes.ProjectData):
    """Находит пост в канале по ссылке и обновляет его (если передана ссылка)."""
    if post_url:
        post_id = post_url.split('/')[-1]
        text = templates.form_post_text(project_status, post_data)
        has_files = bool(post_data.files)
        keyboard = inline_funcs.for_project(project_id, files_btn=has_files)
        await bot.edit_message_text(text, MAIN_CHANNEL, post_id, reply_markup=keyboard)


async def delete_post(post_url: str = None):
    """Удаляет пост из канала, если передана ссылка."""
    if post_url:
        post_id = post_url.split('/')[-1]
        await bot.delete_message(MAIN_CHANNEL, post_id)
