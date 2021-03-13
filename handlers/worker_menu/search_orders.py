from aiogram import types, html
from aiogram.contrib.questions import QuestText
from aiogram.utils.keyboards2 import InlineKeyboard, InlineButton

import functions as funcs
import keyboards as KB
from config import CHANNEL_URL
from loader import dp, users_db


class SearchOrdersKB(InlineKeyboard):
    ALL_ORDERS = InlineButton('Все заказы', url=CHANNEL_URL)
    BY_SUBJECTS = InlineButton('По выбранным предметам', 'orders:search_by_subjects')


@dp.message_handler(text=KB.for_worker.SEARCH_ORDERS)
async def send_search_orders_kb():
    return QuestText('Какие заказы вас интересуют?', SearchOrdersKB())


@dp.callback_query_handler(button=SearchOrdersKB.BY_SUBJECTS)
async def find_orders(msg: types.Message, user_id):
    account = await users_db.get_account_by_id(user_id)
    if not account.subjects:
        return html.b('Вы еще не выбрали ни одного предмета')

    projects = await users_db.get_projects_by_subjects(account.subjects)
    if projects:
        await msg.answer(html.b('Подходящие заказы:'))
        await funcs.send_projects(projects, pick_btn=True)
    else:
        await msg.answer(html.b('Не найдено подходящих заказов'))
