from aiogram import types

from functions import reviews as funcs
from loader import users_db
from texts import templates


async def remove_button(query: types.CallbackQuery, index: int):
    """Remove one button from linked inline keyboard."""
    msg = query.message
    reply_markup = msg.reply_markup
    reply_markup.inline_keyboard.pop(index)
    await msg.edit_reply_markup(reply_markup)


async def get_full_bid_text(worker_id: types.Message, project_id: str, bid_text: str) -> str:
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

    return templates.form_bid_text(worker_nickname, worker_url, post_url, avg_rating_text, bid_text)
