"""Инлайновые клавиатуры с генерацией данных."""

from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.helper import Helper, Item
from config import START_LINK
from loader import calendar

DEL_MESSAGE_DATA = 'DEL_MESSAGE'  # для удаления связанного сообщения


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


class InlineKeyboard(InlineKeyboardMarkup, Helper):
    def data_row(self, text: str, callback_data: str):
        self.row(Button(text, callback_data=callback_data))

    def url_row(self, text: str, url: str):
        self.row(Button(text, url=url))


def link_button(text: str, url: str):
    """Одна кнопка-ссылка."""
    keyboard = InlineKeyboard()
    keyboard.url_row(text, url)
    return keyboard


def for_project(project_id: str, pick_btn=False, del_btn=False, files_btn=False, chat_link=None):
    """Кнопки с данными в формате: prefix{project_id} + кнопка-ссылка в чат."""
    keyboard = InlineKeyboard()

    def add_button(text, prefix, as_url=True):
        if as_url:
            url = START_LINK.format(prefix + project_id)
            keyboard.url_row(text, url)
        else:
            cdata = prefix + project_id
            keyboard.data_row(text, cdata)

    if pick_btn:
        add_button('Взять проект', Prefixes.SEND_BID_)
    if files_btn:
        add_button('Посмотреть файлы', Prefixes.GET_FILES_)
    if del_btn:
        add_button('Удалить проект', Prefixes.DEL_PROJECT_, as_url=False)
    if chat_link:
        keyboard.url_row('Перейти в чат', chat_link)
    return keyboard


def del_project(project_id: str):
    """Для окончательного удаления проекта."""
    keyboard = InlineKeyboard()
    cdata = Prefixes.TOTAL_DEL_PROJECT_ + project_id
    keyboard.data_row('Удалить проект', cdata)
    keyboard.data_row('Отменить', DEL_MESSAGE_DATA)
    return keyboard


def for_bid(bid_id: str, pick_btn=True, refuse_btn=True):
    """Кнопки c данными в формате: {prefix}{bid_id}."""
    keyboard = InlineKeyboard()
    pick_bid_data = Prefixes.PICK_BID_ + bid_id

    if pick_btn:
        keyboard.data_row('Принять завку', pick_bid_data)
    if refuse_btn:
        keyboard.data_row('Отклонить', DEL_MESSAGE_DATA)
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
