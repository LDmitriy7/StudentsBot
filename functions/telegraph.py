from loader import bot, users_db
from utils import telegraph_api
from keyboards.inline_funcs import Prefixes
from aiogram.utils.deep_linking import get_start_link
from typing import List


async def get_file_urls(file_ids: list) -> List[str]:
    return [await (await bot.get_file(file_id)).get_url() for file_id in file_ids]


async def get_invite_project_url(user_id: int) -> str:
    """Создает ссылку-приглашение в личный проект."""
    payload = f'{Prefixes.OFFER_PROJECT_}{user_id}'
    return await get_start_link(payload)


async def create_author_page(user_id: int) -> str:
    """Create or edit author page and return page_url."""
    account = await users_db.get_account_by_id(user_id)
    reviews = await users_db.get_reviews_by_worker(user_id)

    p = account['profile']
    page_url = account.get('page_url')
    photo_urls = await get_file_urls(p['works'])
    invite_project_url = await get_invite_project_url(user_id)

    html_content = telegraph_api.make_html_content(
        p['deals_amount'], p['biography'], account['subjects'],
        invite_project_url, photo_urls, reviews
    )

    page_url = telegraph_api.create_page(p['nickname'], html_content, page_url)
    return page_url
