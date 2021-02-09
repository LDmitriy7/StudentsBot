from aiogram import types

from functions import reviews as funcs
from keyboards import inline_funcs
from loader import users_db, bot
from texts import templates


async def get_worker_bid_text(worker_id: types.Message, project_id: str, bid_text: str) -> str:
    """Формирует полный текст для заявки."""
    worker_account = await users_db.get_account_by_id(worker_id)
    reviews = await users_db.get_reviews_by_worker(worker_id)
    project = await users_db.get_project_by_id(project_id)
    avg_rating = funcs.count_avg_rating(reviews)
    avg_rating_text = templates.form_avg_rating_text(avg_rating)

    profile = worker_account['profile']
    post_url = project['post_url']
    worker_nickname = profile['nickname']
    worker_url = worker_account['page_url']

    return templates.form_worker_bid_text(worker_nickname, worker_url, post_url, avg_rating_text, bid_text)


async def send_client_bid(client_name: str, worker_id: int, bid_id: str):
    """Отправляет заявку исполнителю от клиента."""
    bid_text: str = templates.form_client_bid_text(client_name)
    keyboard = inline_funcs.for_bid(bid_id)
    await bot.send_message(worker_id, bid_text, reply_markup=keyboard)
