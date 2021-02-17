from dataclasses import asdict, fields
from typing import List, Optional

from aiogram import types

from config import CHANNEL_USERNAME, CHANNEL_POST_URL, BOT_START_LINK
from data_types import Prefixes, Update, data_classes
from keyboards import inline_funcs
from loader import bot, users_db
from texts import templates
import subfuncs

__all__ = ['count_avg_rating', 'get_invite_project_url', 'get_chat_link', 'get_all_nicknames',
           'send_post', 'update_post', 'delete_post', 'get_chat_of_update']


async def get_chat_link(chat_id: int) -> Optional[str]:
    """Return chat link if chat exists."""
    chat = await users_db.get_chat_by_id(chat_id)
    return chat.link if chat else None


def get_invite_project_url(user_id: int) -> str:
    """Создает ссылку-приглашение в личный проект."""
    payload = f'{Prefixes.INVITE_PROJECT_}{user_id}'
    return BOT_START_LINK.format(payload)


def count_avg_rating(reviews: List[data_classes.Review]) -> dict:
    """Count average user's rating dict from reviews."""
    all_fields = [field.name for field in fields(data_classes.Rating)]
    rating_dicts = [asdict(r.rating) for r in reviews]
    return subfuncs.count_avg_values(rating_dicts, all_fields)


async def get_all_nicknames() -> set:
    """Возращает набор всех никнеймов в коллекции аккаунтов."""
    nicknames = set()
    for a in await users_db.get_all_accounts():
        if a.profile:
            nicknames.add(a.profile.nickname)
    return nicknames


# posts


async def send_post(
        project_id: str, project_status: str, post_data: data_classes.ProjectData
) -> str:
    """Send post to channel. Return post_url."""
    text = templates.form_post_text(project_status, post_data)
    has_files = bool(post_data.files)
    keyboard = inline_funcs.for_project(project_id, pick_btn=True, files_btn=has_files)

    post_obj = await bot.send_message(CHANNEL_USERNAME, text, reply_markup=keyboard)
    post_url = CHANNEL_POST_URL.format(post_obj.message_id)
    return post_url


async def update_post(project_id: str, project_status: str, post_url: Optional[str],
                      post_data: data_classes.ProjectData):
    """Находит пост в канале по ссылке и обновляет его (если передана ссылка)."""
    if post_url:
        post_id = post_url.split('/')[-1]
        text = templates.form_post_text(project_status, post_data)
        has_files = bool(post_data.files)
        keyboard = inline_funcs.for_project(project_id, files_btn=has_files)
        await bot.edit_message_text(text, CHANNEL_USERNAME, post_id, reply_markup=keyboard)


async def delete_post(post_url: str = None):
    """Удаляет пост из канала, если передана ссылка."""
    if post_url:
        post_id = post_url.split('/')[-1]
        await bot.delete_message(CHANNEL_USERNAME, post_id)
