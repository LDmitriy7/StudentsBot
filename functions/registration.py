from functions._telegraph import create_author_page
from loader import users_db
import datatypes as datatypes


async def save_profile(user_id: int, profile_data: dict, nickname: str, deals_amount=0):
    """Сохраняет профиль в базу, создает страницу автора."""
    profile = datatypes.Profile(**profile_data, nickname=nickname, deals_amount=deals_amount)
    await users_db.update_account_profile(user_id, profile)
    page_url = await create_author_page(user_id)  # создаем страницу автора
    await users_db.update_account_page_url(user_id, page_url)
