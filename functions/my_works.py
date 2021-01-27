from aiogram import types
from texts import templates
from typing import List
from keyboards import inline_func


async def send_bids(msg: types.Message, bids: List[dict]):
    for b in bids:
        project_id = b['project_id']
        bid_id = str(b['_id'])
        bid_text = b['text']
        text = templates.form_bid_text('Имя', 'https://test.com', bid_text)
        keyboard = inline_func.for_bid(project_id, bid_id, pick_bid_btn=False, refuse_bid_btn=False)
        await msg.answer(text, reply_markup=keyboard)
