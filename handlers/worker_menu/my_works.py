from aiogram import types
from aiogram.contrib.questions import QuestText
from aiogram.utils.keyboards2 import InlineButton, InlineKeyboard
from aiogram.utils.markdown import hbold as b

import functions as funcs
import keyboards as KB
from data_types import ProjectStatuses
from loader import dp, users_db


class MyWorks(InlineKeyboard):
    ACTIVE = InlineButton('Активные проекты', callback='works:send:active')
    IN_PROGRESS = InlineButton('Проекты в работе', callback='works:send:in_progress')


my_works = MyWorks()


@dp.message_handler(text=KB.for_worker.MY_WORKS)
async def ask_works_type():
    return QuestText('Выберите тип работ', my_works)


@dp.callback_query_handler(button=my_works.ACTIVE)
async def send_active_works(msg: types.Message, user_id):
    """
    1) Найти и отправить все активные проекты, персональные или с заявкой исполнителя, от новых к старым
    2) Добавить к каждому кнопки: файлы, ссылка в чат
    """

    bids = await users_db.get_bids_by_user(worker_id=user_id)
    projects = [await users_db.get_project_by_id(bid.project_id) for bid in bids]
    fit_works = [p for p in projects if p and p.status == ProjectStatuses.ACTIVE]

    personal_works = await users_db.get_projects_by_user(worker_id=user_id)
    active_works = [p for p in personal_works if p.status == ProjectStatuses.ACTIVE]
    fit_works.extend(active_works)

    if fit_works:
        fit_works = reversed(fit_works)
        await msg.answer(b('Список активных проектов:'))
        await funcs.send_projects(fit_works, worker_chat_btn=True)
    else:
        await msg.answer('У вас нет заявок ни на один проект')


@dp.callback_query_handler(button=my_works.IN_PROGRESS)
async def send_works_in_progress(msg: types.Message, user_id):
    """
    1) Найти и отправить все проекты в работе, от новых к старым
    2) Добавить к каждому кнопки: файлы, ссылка в чат
    """

    projects = await users_db.get_projects_by_user(worker_id=user_id)
    fit_works = [p for p in projects if p and p.status == ProjectStatuses.IN_PROGRESS]

    if fit_works:
        fit_works = reversed(fit_works)
        await msg.answer(b('Список проектов в работе:'))
        await funcs.send_projects(fit_works, worker_chat_btn=True)
    else:
        await msg.answer('У вас нет проектов в работе')
