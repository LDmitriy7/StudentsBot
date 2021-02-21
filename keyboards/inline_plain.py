"""Простые инлайновые клавиатуры."""

from dataclasses import dataclass
from typing import Optional
from aiogram.types import InlineKeyboardButton as IButton

from data_types.constants import TextQueries
from data_types.keyboards import InlineKeyboard, InlineButton, SameInlineKeyboard

_B = Optional[InlineButton]


class WorkTypeKeyboard(SameInlineKeyboard):
    BUTTONS = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая',
        'Дипломная', 'Практика', 'Эссе', 'Доклад', 'Статья', 'Тезисы',
        'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]


@dataclass
class MyProfileKeyboard(InlineKeyboard):
    CHANGE_NICKNAME: _B = InlineButton('Изменить никнейм')
    CHANGE_PHONE_NUMBER: _B = InlineButton('Изменить телефон')
    CHANGE_EMAIL: _B = InlineButton('Изменить email')
    CHANGE_BIOGRAPHY: _B = InlineButton('Изменить биографию')
    CHANGE_WORKS: _B = InlineButton('Изменить примеры работ')


@dataclass
class BalanceKeyboard(InlineKeyboard):
    DEPOSIT_MONEY: _B = InlineButton('Пополнить баланс')
    WITHDRAW_MONEY: _B = InlineButton('Вывести деньги')


@dataclass
class UserRolesKeyboard(InlineKeyboard):
    CLIENT: _B = InlineButton('Я заказчик')
    WORKER: _B = InlineButton('Я исполнитель')


@dataclass
class SubjectsKeyboard(InlineKeyboard):
    CHANGE_SUBJECTS: _B = InlineButton('Изменить предметы')


# для поиска предметов
find_subject = InlineKeyboard()
find_subject.row(IButton('Найти предмет', switch_inline_query_current_chat=''))

# для предложения проекта заказчику
invite_project = InlineKeyboard()
invite_project.row(IButton('Выбрать чат', switch_inline_query=TextQueries.INVITE_PROJECT))
