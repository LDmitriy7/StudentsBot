"""Инлайновые клавиатуры с генерацией данных."""

import re
from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton as InlineButton
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard
from aiogram.utils.deep_linking import get_start_link

from loader import calendar

DEL_MESSAGE_DATA = 'del_message'  # для удаления связанного сообщения

TOTAL_DEL_PROJECT_PREFIX = 'del_total_project_'  # для удаления проекта
DEL_PROJECT_PREFIX = 'del_project_'  # для запроса удаления проекта
GET_PROJECT_PREFIX = 'get_project_'  # для получения проекта
PAY_FOR_PROJECT_PREFIX = 'pay_for_project_'  # для оплаты проекта
GET_FILES_PREFIX = 'get_files_'  # для получения файлов к проекту

SEND_BID_PREFIX = 'send_bid_'  # для заявки на проект
PICK_BID_PREFIX = 'pick_bid_'  # для принятия заявки

ALL_PREFIXES = [
    TOTAL_DEL_PROJECT_PREFIX, DEL_PROJECT_PREFIX, GET_PROJECT_PREFIX, PAY_FOR_PROJECT_PREFIX,
    GET_FILES_PREFIX, SEND_BID_PREFIX, PICK_BID_PREFIX
]

SEND_BID_PATTERN = re.compile(f'{SEND_BID_PREFIX}[0-9a-f]+')
GET_FILES_PATTERN = re.compile(f'{GET_FILES_PREFIX}[0-9a-f]+')


def get_payload(text: str) -> str:
    """Delete all possible prefixes and return project_id."""
    payload = text.split()[-1]
    for prefix in ALL_PREFIXES:
        payload = payload.replace(prefix, '')
    return payload


async def for_project(project_id: str, pick_button=False, del_button=False, files_button=False):
    """Кнопки с данными в формате: prefix{project_id}"""
    keyboard = InlineKeyboard()

    async def add_button(text, prefix):
        url = await get_start_link(prefix + project_id)
        keyboard.row(InlineButton(text, url=url))

    if pick_button:
        await add_button('Взять проект', SEND_BID_PREFIX)

    if files_button:
        await add_button('Посмотреть файлы', GET_FILES_PREFIX)

    if del_button:
        cdata = DEL_PROJECT_PREFIX + project_id
        keyboard.row(InlineButton('Удалить проект', callback_data=cdata))

    return keyboard


def delete_project(project_id: str):
    keyboard = InlineKeyboard()
    cdata = TOTAL_DEL_PROJECT_PREFIX + project_id
    keyboard.row(InlineButton('Удалить проект', callback_data=cdata))
    keyboard.row(InlineButton('Отменить', callback_data=DEL_MESSAGE_DATA))
    return keyboard


def for_bid(project_id: str, bid_id: str, pick_bid_btn=True, refuse_bid_btn=True):
    keyboard = InlineKeyboard()
    cdata1 = GET_PROJECT_PREFIX + project_id
    cdata2 = PICK_BID_PREFIX + bid_id
    keyboard.row(InlineButton('Посмотреть проект', callback_data=cdata1))
    if pick_bid_btn:
        keyboard.row(InlineButton('Принять завку', callback_data=cdata2))
    if refuse_bid_btn:
        keyboard.row(InlineButton('Отклонить', callback_data=DEL_MESSAGE_DATA))
    return keyboard


def get_calendar():
    days_names = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    month_names = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
        'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    calendar.init(
        date.today(),
        min_date=date.today(),
        max_date=date.today() + timedelta(weeks=30),
        days_names=days_names,
        month_names=month_names
    )
    return calendar.get_keyboard()
