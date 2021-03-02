from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.utils.keyboards2 import IButton, InlineKeyboard
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses
from loader import dp, users_db


class MyOrders(InlineKeyboard):
    ACTIVE = IButton('Активные проекты', callback='orders:send:active')
    IN_PROGRESS = IButton('Проекты на выполнении', callback='orders:send:in_progress')


my_orders = MyOrders()


@dp.message_handler(text=KB.main.MY_ORDERS)
async def ask_orders_type():
    return QuestText('Выберите тип заказов', my_orders)


@dp.callback_query_handler(text=my_orders.ACTIVE)
async def send_active_orders(msg: types.Message, user_id):
    """
    1) найти и отправить все активные проекты клиента от новых к старым
    2) добавить к каждому заметку и кнопки: файлы, ссылки в чаты, удаление
    """

    projects = await users_db.get_projects_by_user(client_id=user_id)
    active_projects = [p for p in projects if p.status == ProjectStatuses.ACTIVE]

    if active_projects:
        active_projects = reversed(active_projects)
        await msg.answer(b('Список активных заказов:'))
        await funcs.send_projects(active_projects, with_note=True, del_btn=True, client_chat_btns=True)
    else:
        await msg.answer(b('У вас нет ни одного активного заказа'))


@dp.callback_query_handler(text=my_orders.IN_PROGRESS)
async def send_orders_in_progress(msg: types.Message, user_id):
    """
    1) найти и отправить все проекты клиента на выполнении, от новых к старым
    2) добавить к каждому заметку и кнопки: файлы, ссылку в рабочий чат
    """

    projects = await users_db.get_projects_by_user(client_id=user_id)
    fit_projects = [p for p in projects if p.status == ProjectStatuses.IN_PROGRESS]

    if fit_projects:
        fit_projects = reversed(fit_projects)
        await msg.answer(b('Список заказов на выполнении:'))
        await funcs.send_projects(fit_projects, with_note=True, client_chat_btns=True)
    else:
        await msg.answer(b('У вас нет ни одного заказа в работе'))
