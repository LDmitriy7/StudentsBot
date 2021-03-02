"""Contain funcs for work with telegraph."""
from typing import List

from aiogram.dispatcher.currents import CurrentObjects

from functions.common import count_avg_rating, get_invite_project_url
from loader import bot, users_db
from utils import telegraph_api

__all__ = ['save_author_page']


async def get_file_urls(file_ids: list) -> List[str]:
    """Возращает список ссылок на файлы по их айди."""
    return [await (await bot.get_file(file_id)).get_url() for file_id in file_ids]


@CurrentObjects.decorate
async def save_author_page(*, user_id) -> str:
    """Create or edit author page, save and return page_url."""
    account = await users_db.get_account_by_id(user_id)
    reviews = await users_db.get_reviews_by_worker(user_id)

    p = account.profile
    photo_urls = await get_file_urls(p.works)
    invite_project_url = get_invite_project_url(user_id)
    avg_rating = count_avg_rating(reviews)

    html_content = await telegraph_api.make_html_content(
        p.deals_amount, p.biography, account.subjects,
        invite_project_url, photo_urls, avg_rating, reviews
    )
    page_url = await telegraph_api.create_page(p.nickname, html_content, account.page_url)
    await users_db.update_account_page_url(user_id, page_url)
    return page_url
