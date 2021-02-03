"""Инлайновые клавиатуры с генерацией данных."""

from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.helper import Item, Helper
from loader import calendar

DEL_MESSAGE_DATA = 'del_message'  # для удаления связанного сообщения


class Prefixes(Helper):
    """Command-prefixes for deep-links and query.data"""
    GET_PROJECT_ = Item()  # для получения проекта
    DEL_PROJECT_ = Item()  # для запроса удаления проекта
    TOTAL_DEL_PROJECT_ = Item()  # для удаления проекта
    PAY_FOR_PROJECT_ = Item()  # для оплаты проекта
    OFFER_PROJECT_ = Item()  # для предложения личного проекта

    GET_FILES_ = Item()  # для получения файлов к проекту

    SEND_BID_ = Item()  # для заявки на проект
    PICK_BID_ = Item()  # для принятия заявки


async def for_project(project_id: str, pick_btn=False, del_btn=False, files_btn=False):
    """Кнопки с данными в формате: prefix{project_id}"""
    keyboard = InlineKeyboard()

    async def add_button(text, prefix, as_url=True):
        if as_url:
            url = await get_start_link(prefix + project_id)
            button = Button(text, url=url)
        else:
            cdata = prefix + project_id
            button = Button(text, callback_data=cdata)
        keyboard.row(button)

    if pick_btn:
        await add_button('Взять проект', Prefixes.SEND_BID_)

    if files_btn:
        await add_button('Посмотреть файлы', Prefixes.GET_FILES_)

    if del_btn:
        await add_button('Удалить проект', Prefixes.DEL_PROJECT_, as_url=False)

    return keyboard


def delete_project(project_id: str):
    """Для окончательного удаления проекта."""
    keyboard = InlineKeyboard()
    cdata = Prefixes.TOTAL_DEL_PROJECT_ + project_id
    keyboard.row(Button('Удалить проект', callback_data=cdata))
    keyboard.row(Button('Отменить', callback_data=DEL_MESSAGE_DATA))
    return keyboard


def for_bid(project_id: str, bid_id: str, watch_project_btn=True, pick_bid_btn=True, refuse_bid_btn=True):
    """Кнопки c данными в формате: {prefix}{object_id}."""
    keyboard = InlineKeyboard()
    get_project_data = Prefixes.GET_PROJECT_ + project_id
    pick_bid_data = Prefixes.PICK_BID_ + bid_id

    if watch_project_btn:
        keyboard.row(Button('Посмотреть проект', callback_data=get_project_data))
    if pick_bid_btn:
        keyboard.row(Button('Принять завку', callback_data=pick_bid_data))
    if refuse_bid_btn:
        keyboard.row(Button('Отклонить', callback_data=DEL_MESSAGE_DATA))

    return keyboard


def make_calendar():
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
