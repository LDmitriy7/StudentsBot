"""Инлайновые клавиатуры с генерацией данных."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

from aiogram.types import InlineKeyboardButton as Button

from config import BOT_START_LINK
from data_types import Prefixes, TextQueries
from data_types.keyboards import InlineKeyboard, InlineButton
from loader import calendar

_B = Optional[InlineButton]


@dataclass
class GroupMenu(InlineKeyboard):
    CALL_ADMIN: _B = InlineButton('Вызвать админа')
    OFFER_PRICE: _B = InlineButton('Предложить цену')
    CONFIRM_PROJECT: _B = InlineButton('Подтвердить выполнение')
    FEEDBACK: _B = InlineButton('Оставить отзыв')


def link_button(text: str, url: str):
    """Одна кнопка-ссылка."""
    keyboard = InlineKeyboard()
    keyboard.url_row(text, url)
    return keyboard


def invite_project(worker_id: int):
    """Кнопка 'Заполнить проект' со стартовой ссылкой {prefix}{worker_id}."""
    keyboard = InlineKeyboard()
    url = BOT_START_LINK.format(f'{Prefixes.INVITE_PROJECT_}{worker_id}')
    keyboard.url_row('Заполнить проект', url)
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


def del_project(project_id: str):
    """Для окончательного удаления проекта."""
    keyboard = InlineKeyboard()
    cdata = f'{Prefixes.TOTAL_DEL_PROJECT_}{project_id}'
    keyboard.data_row('Удалить проект', cdata)
    keyboard.data_row('Отменить', TextQueries.DEL_MESSAGE)
    return keyboard


def pay_for_project(price: int, project_id: str):
    """Кнопки: Оплатить(prefix_price_project), Отказаться."""
    keyboard = InlineKeyboard()
    cdata = f'{Prefixes.PAY_FOR_PROJECT_}{price}_{project_id}'
    keyboard.data_row(f'Оплатить {price} грн', cdata)
    keyboard.data_row('Отказаться', TextQueries.REFUSE_WORK_PRICE)
    return keyboard


def total_confirm_project(project_id: str):
    """Кнопки: Подтвердить(prefix_project), Отменить."""
    keyboard = InlineKeyboard()
    cdata = f'{Prefixes.CONFIRM_PROJECT_}{project_id}'
    keyboard.data_row('Подтвердить', cdata)
    keyboard.data_row('Отменить', TextQueries.DEL_MESSAGE)
    return keyboard


def for_project(project_id: str, pick_btn=False, del_btn=False, files_btn=False, chat_link=None):
    """Кнопки с данными в формате: prefix{project_id} + кнопка-ссылка в чат."""
    keyboard = InlineKeyboard()

    def add_button(text, prefix, as_url=True):
        if as_url:
            url = BOT_START_LINK.format(f'{prefix}{project_id}')
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


def for_bid(bid_id: str, pick_btn=True, refuse_btn=True):
    """Кнопки c данными в формате: {prefix}{bid_id}."""
    keyboard = InlineKeyboard()
    pick_bid_data = f'{Prefixes.PICK_BID_}{bid_id}'

    if pick_btn:
        button1 = Button('Принять', callback_data=pick_bid_data)
        keyboard.insert(button1)
    if refuse_btn:
        button2 = Button('Отклонить', callback_data=TextQueries.DEL_MESSAGE)
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
