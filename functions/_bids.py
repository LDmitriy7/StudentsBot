from dataclasses import asdict, fields

from aiogram.dispatcher.currents import CurrentObjects

import subfuncs
from data_types import data_models
from keyboards import inline_funcs
from loader import users_db, bot
from texts import templates

__all__ = ['get_worker_bid_text', 'send_chat_link']


@CurrentObjects.decorate
async def get_worker_bid_text(project_id: str, *, user_id, text) -> str:
    """Формирует полный текст для заявки исполнителя на проект."""
    account = await users_db.get_account_by_id(user_id)
    reviews = await users_db.get_reviews_by_worker(user_id)
    project = await users_db.get_project_by_id(project_id)

    ratings = [asdict(r.rating) for r in reviews]
    rates = [f.name for f in fields(data_models.Rating)]
    avg_rating = subfuncs.count_avg_values(ratings, rates)
    avg_rating_text = templates.form_avg_rating_text(avg_rating)

    return templates.form_worker_bid_text(
        account.profile.nickname,
        account.page_url,
        project.post_url,
        avg_rating_text,
        text,
    )


async def send_chat_link(user_id: int, msg_text: str, chat_link):
    keyboard = inline_funcs.link_button('Перейти в чат', chat_link)
    await bot.send_message(user_id, msg_text, reply_markup=keyboard)
