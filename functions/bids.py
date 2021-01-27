from aiogram.dispatcher import FSMContext
from loader import users_db, bot
from texts import templates
from aiogram import types
from typing import Tuple


async def get_full_bid(bid_text: str, state: FSMContext) -> Tuple[dict, str]:
    """Return dict: bid_data and text: bid_text_result."""
    udata = await state.get_data()

    project_id = udata['project_id']
    project = await users_db.get_project_by_id(project_id)

    post_url = project['post_url']
    note = project['data']['note']
    worker_name = udata['worker_name']

    bid_data = dict(
        client_id=project['client_id'],
        worker_id=udata['worker_id'],
        project_id=project_id,
    )

    bid_text_data = dict(
        worker_url='',
        worker_nickname=worker_name,
        post_url=post_url,
        bid_text=bid_text,
        note=note,
    )
    bid_text_result = templates.form_bid_text(bid_text_data)
    return bid_data, bid_text_result


async def remove_button(query: types.CallbackQuery, index: int):
    msg = query.message
    reply_markup = msg.reply_markup
    reply_markup.inline_keyboard.pop(index)
    await msg.edit_reply_markup(reply_markup)
