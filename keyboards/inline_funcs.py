"""Инлайновые клавиатуры с генерацией данных."""

from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.helper import Helper

from config import START_LINK
from datatypes import Prefixes
from loader import calendar

DEL_MESSAGE_DATA = 'DEL_MESSAGE'  # для удаления связанного сообщения


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


def offer_project(project_id: str):
    """Кнопка 'Выбрать чат' для отправки проекта лично."""
    keyboard = InlineKeyboard()
    siq = f'{Prefixes.OFFER_PROJECT_}{project_id}'
    keyboard.row(Button('Выбрать чат', switch_inline_query=siq))
    return keyboard


def pick_project(project_id: str):
    """Кнопка 'Позвать в чат' для принятия проекта автором."""
    keyboard = InlineKeyboard()
    cdata = f'{Prefixes.PICK_PROJECT_}{project_id}'
    keyboard.data_row('Позвать в чат', cdata)
    return keyboard


def invite_project(worker_id: int):
    """Кнопка 'Заполнить проект' со стартовой ссылкой {prefix}{worker_id}."""
    keyboard = InlineKeyboard()
    url = START_LINK.format(f'{Prefixes.INVITE_PROJECT_}{worker_id}')
    keyboard.url_row('Заполнить проект', url)
    return keyboard


def for_project(project_id: str, pick_btn=False, del_btn=False, files_btn=False, chat_link=None):
    """Кнопки с данными в формате: prefix{project_id} + кнопка-ссылка в чат."""
    keyboard = InlineKeyboard()

    def add_button(text, prefix, as_url=True):
        if as_url:
            url = START_LINK.format(f'{prefix}{project_id}')
            keyboard.url_row(text, url)
        else:
            cdata = f'{prefix}{project_id}'
            keyboard.data_row(text, cdata)

    if pick_btn:
        add_button('Взять проект', Prefixes.SEND_BID_)
    if files_btn:
        add_button('Посмотреть файлы', Prefixes.GET_FILES_)
    if chat_link:
        keyboard.url_row('Перейти в чат', chat_link)
    if del_btn:
        add_button('Удалить проект', Prefixes.DEL_PROJECT_, as_url=False)
    return keyboard


def del_project(project_id: str):
    """Для окончательного удаления проекта."""
    keyboard = InlineKeyboard()
    cdata = f'{Prefixes.TOTAL_DEL_PROJECT_}{project_id}'
    keyboard.data_row('Удалить проект', cdata)
    keyboard.data_row('Отменить', DEL_MESSAGE_DATA)
    return keyboard


def for_bid(bid_id: str, pick_btn=True, refuse_btn=True):
    """Кнопки c данными в формате: {prefix}{bid_id}."""
    keyboard = InlineKeyboard()
    pick_bid_data = f'{Prefixes.PICK_BID_}{bid_id}'

    if pick_btn:
        button1 = Button('Принять', callback_data=pick_bid_data)
        keyboard.insert(button1)
    if refuse_btn:
        button2 = Button('Отклонить', callback_data=DEL_MESSAGE_DATA)
        keyboard.insert(button2)
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
