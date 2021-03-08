from aiogram.contrib.middlewares.conversation import UpdateData
from aiogram import html

import functions as funcs
import keyboards as KB
from filters import find_pair_chat
from loader import dp, bot
from questions import FeedbackConv


@dp.callback_query_handler(text=KB.GroupMenu.FEEDBACK)
async def start_feedback():
    return UpdateData(new_state=FeedbackConv)


@dp.callback_query_handler(text=KB.rates.BUTTONS, state=FeedbackConv.ask_quality)
async def process_quality(data: str):
    amount = int(data.split()[0])
    return UpdateData({'quality': amount})


@dp.callback_query_handler(text=KB.rates.BUTTONS, state=FeedbackConv.ask_terms)
async def process_terms(data: str):
    amount = int(data.split()[0])
    return UpdateData({'terms': amount})


@dp.callback_query_handler(text=KB.rates.BUTTONS, state=FeedbackConv.ask_contact)
async def process_contact(data: str):
    amount = int(data.split()[0])
    return UpdateData({'contact': amount})


@dp.message_handler(find_pair_chat, state=FeedbackConv.ask_text)
async def process_review_text(pchat_id: int):
    review = await funcs.save_review()
    await funcs.save_author_page(user_id=review.worker_id)
    await bot.send_message(pchat_id, html.b('Заказчик оставил отзыв на вашей странице'))
    return UpdateData(), html.b('Отзыв оставлен')
