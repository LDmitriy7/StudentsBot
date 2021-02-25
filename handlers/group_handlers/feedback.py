from aiogram import types
from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from filters import find_pair_chat
from loader import dp, bot
from questions import FeedbackConv


@dp.callback_query_handler(text=KB.GroupMenu.FEEDBACK)
async def start_feedback():
    return UpdateData(new_state=FeedbackConv)


@dp.callback_query_handler(text=KB.Rates.BUTTONS, state=FeedbackConv.ask_quality)
async def process_quality(data):
    return UpdateData({'quality': int(data)})


@dp.callback_query_handler(text=KB.Rates.BUTTONS, state=FeedbackConv.ask_terms)
async def process_terms(data):
    return UpdateData({'terms': int(data)})


@dp.callback_query_handler(text=KB.Rates.BUTTONS, state=FeedbackConv.ask_contact)
async def process_contact(data):
    return UpdateData({'contact': int(data)})


@dp.message_handler(find_pair_chat, state=FeedbackConv.ask_text)
async def process_review_text(pchat_id: int):
    await funcs.save_review()
    await bot.send_message(pchat_id, b('Заказчик оставил отзыв на вашей странице'))
    return UpdateData(), b('Отзыв оставлен')
