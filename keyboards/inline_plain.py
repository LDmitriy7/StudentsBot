"""Простые инлайновые клавиатуры."""

from dataclasses import dataclass
from typing import Optional

from aiogram.types import InlineKeyboardButton as IButton

from data_types.constants import TextQueries
from data_types.keyboards import InlineKeyboard, InlineButton, SameInlineKeyboard

__all__ = [
    'WorkTypes', 'MyProfile', 'Balance', 'UserRoles', 'Subjects',
    'find_subject', 'choose_invite_chat', 'Rates'
]

_B = Optional[InlineButton]


class Rates(SameInlineKeyboard):
    BUTTONS = ['1', '2', '3', '4', '5']


class WorkTypes(SameInlineKeyboard):
    BUTTONS = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая',
        'Дипломная', 'Практика', 'Эссе', 'Доклад', 'Статья', 'Тезисы',
        'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]


@dataclass
class MyProfile(InlineKeyboard):
    CHANGE_NICKNAME: _B = InlineButton('Изменить никнейм')
    CHANGE_PHONE_NUMBER: _B = InlineButton('Изменить телефон')
    CHANGE_EMAIL: _B = InlineButton('Изменить email')
    CHANGE_BIOGRAPHY: _B = InlineButton('Изменить биографию')
    CHANGE_WORKS: _B = InlineButton('Изменить примеры работ')


@dataclass
class Balance(InlineKeyboard):
    DEPOSIT_MONEY: _B = InlineButton('Пополнить баланс')
    WITHDRAW_MONEY: _B = InlineButton('Вывести деньги')


@dataclass
class UserRoles(InlineKeyboard):
    CLIENT: _B = InlineButton('Я заказчик')
    WORKER: _B = InlineButton('Я исполнитель')


@dataclass
class Subjects(InlineKeyboard):
    CHANGE_SUBJECTS: _B = InlineButton('Изменить предметы')


# для поиска предметов
find_subject = InlineKeyboard()
find_subject.row(IButton('Найти предмет', switch_inline_query_current_chat=''))

# для предложения проекта заказчику
choose_invite_chat = InlineKeyboard()
choose_invite_chat.row(IButton('Выбрать чат', switch_inline_query=TextQueries.INVITE_PROJECT))
