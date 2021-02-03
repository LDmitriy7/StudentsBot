from loader import users_db, bot
from utils import telegraph_api as telegraph
from keyboards.inline_func import Prefixes
from aiogram.utils.deep_linking import get_start_link


async def get_all_nicknames() -> set:
    """Возращает сет всех никнеймов пользователей."""
    all_nicknames = set()
    for account in await users_db.get_all_accounts():
        profile = account.get('profile')
        if profile:
            nickname = profile['nickname']
            all_nicknames.add(nickname)
    return all_nicknames


async def get_file_urls(file_ids: list) -> list:
    return [await (await bot.get_file(file_id)).get_url() for file_id in file_ids]


async def create_author_page(user_id: int) -> str:
    """Create initial author page and return page_url."""
    account = await users_db.get_account_by_id(user_id)
    p = account['profile']
    photo_urls = await get_file_urls(p['works'])
    offer_project_url = await get_start_link(f'{Prefixes.OFFER_PROJECT_}{user_id}')

    html_content = telegraph.make_html_content(
        0, p['biography'], [], offer_project_url, photo_urls, []
    )

    page_url = telegraph.create_page(p['nickname'], html_content)
    return page_url
