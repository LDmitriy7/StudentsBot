"""Инлайновые клавиатуры с генерацией данных."""

from datetime import timedelta, datetime

import pytz
from aiogram.utils.keyboards2 import InlineKeyboard, InlineButton

from loader import calendar

DEL_MESSAGE = 'del:message'


class GroupMenu(InlineKeyboard):
    CALL_ADMIN = 'Вызвать админа'
    OFFER_PRICE = 'Предложить цену'
    CONFIRM_PROJECT = 'Подтвердить выполнение'
    FEEDBACK = 'Оставить отзыв'

    def __init__(self, call_admin: bool, offer_price: bool, confirm_project: bool, feedback: bool):
        if not call_admin:
            self.CALL_ADMIN = None
        if not offer_price:
            self.OFFER_PRICE = None
        if not confirm_project:
            self.CONFIRM_PROJECT = None
        if not feedback:
            self.FEEDBACK = None

        super().__init__()


def link_button(text: str, url: str):
    """Одна кнопка-ссылка."""
    keyboard = InlineKeyboard()
    keyboard.url_row(text, url)
    return keyboard


class InviteProject(InlineKeyboard):
    """Кнопка 'Заполнить проект' со стартовой ссылкой {prefix}{worker_id}."""
    START_LINK = InlineButton('Заполнить проект', start_param='project-invite_from-')

    def __init__(self, worker_id: int):
        self.START_LINK += str(worker_id)
        super().__init__()


class OfferProject(InlineKeyboard):
    OFFER = InlineButton('Выбрать чат', switch_iquery='offer:project:')

    def __init__(self, project_id: str):
        self.OFFER += project_id
        super().__init__()


class PickProject(InlineKeyboard):
    PICK = InlineButton('Принять проект', 'project:pick:')
    DEL_MESSAGE = InlineButton('Отменить', DEL_MESSAGE)

    def __init__(self, project_id: str):
        self.PICK += project_id
        super().__init__()


class DelProject(InlineKeyboard):
    DEL_PROJECT = InlineButton('Удалить проект', 'project:total_del:')
    DEL_MESSAGE = InlineButton('Отменить', DEL_MESSAGE)

    def __init__(self, project_id: str):
        self.DEL_PROJECT += project_id
        super().__init__()


class PayForProject(InlineKeyboard):
    PAY = InlineButton('Оплатить', 'project:pay_for:')
    REFUSE = InlineButton('Отказаться', 'work_price:refuse')

    def __init__(self, price: int, project_id: str):
        self.PAY += f'{price}_{project_id}'
        super().__init__()


class ConfirmProject(InlineKeyboard):
    CONFIRM = InlineButton('Подтвердить', callback='confirm:project:')
    DEL_MESSAGE = InlineButton('Отменить', callback=DEL_MESSAGE)

    def __init__(self, project_id: str):
        self.CONFIRM += project_id
        super().__init__()


class ForProject(InlineKeyboard):
    PICK = InlineButton('Взять проект', start_param='send-bid-')
    FILES = InlineButton('Посмотреть файлы', start_param='get-files-')
    REPOST = InlineButton('Обновить в канале', callback='post:repost:')
    DELETE = InlineButton('Удалить проект', callback='del:project:')

    def __init__(self, project_id: str,
                 pick_btn=False, del_btn=False, files_btn=False, chat_links: [list] = None, repost_btn=False):
        if pick_btn:
            self.PICK.url += project_id
        else:
            self.PICK = None

        if files_btn:
            self.FILES.url += project_id
        else:
            self.FILES = None

        if del_btn:
            self.DELETE.callback_data += project_id
        else:
            self.DELETE = None

        if repost_btn:
            self.REPOST.callback_data += project_id
        else:
            self.REPOST = None

        super().__init__()

        if chat_links:
            for num, link in enumerate(chat_links, start=1):
                self.url_row(f'Перейти в чат {num}', link)


class ForBid(InlineKeyboard):
    """Кнопки c данными в формате: {prefix}{bid_id}."""
    PICK = InlineButton('Принять', 'bid:pick:')
    DEL_MESSAGE = InlineButton('Отклонить', DEL_MESSAGE)

    def __init__(self, bid_id: str):
        self.PICK += bid_id
        super().__init__(default_width=2)


def make_calendar():
    days_names = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    month_names = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
        'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]

    ukrainian_tz = pytz.timezone('Etc/GMT-2')
    date_now = datetime.now(tz=ukrainian_tz).date()

    calendar.init(
        base_date=date_now,
        min_date=date_now,
        max_date=date_now + timedelta(weeks=30),
        days_names=days_names,
        month_names=month_names
    )
    return calendar.get_keyboard()


class ControlUser(InlineKeyboard):
    PAY = InlineButton('Начислить деньги', callback='user:pay:')
    WITHDRAW = InlineButton('Списать деньги', callback='user:withdraw:')
    WATCH_BALANCE = InlineButton('Посмотреть баланс', callback='user:watch_balance:')
    WATCH_PROFILE = InlineButton('Посмотреть профиль', callback='user:watch_profile:')

    def __init__(self, user_id: int):
        user_id = str(user_id)

        self.PAY += user_id
        self.WITHDRAW += user_id
        self.WATCH_BALANCE += user_id
        self.WATCH_PROFILE += user_id

        super().__init__()
