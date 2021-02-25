"""Простые инлайновые клавиатуры."""

from aiogram.types import InlineKeyboardButton as IButton

from data_types.constants import TextQueries
from data_types.keyboards import InlineKeyboard, SameInlineKeyboard

__all__ = [
    'WorkTypes', 'MyProfile', 'Balance', 'UserRoles', 'Subjects',
    'find_subject', 'choose_invite_chat', 'Rates'
]


class Rates(SameInlineKeyboard):
    BUTTONS = ['1', '2', '3', '4', '5']


class WorkTypes(SameInlineKeyboard):
    buttons = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая',
        'Дипломная', 'Практика', 'Эссе', 'Доклад', 'Статья', 'Тезисы',
        'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]


class MyProfile(InlineKeyboard):
    CHANGE_NICKNAME = 'Изменить никнейм'
    CHANGE_PHONE_NUMBER = 'Изменить телефон'
    CHANGE_EMAIL = 'Изменить email'
    CHANGE_BIOGRAPHY = 'Изменить биографию'
    CHANGE_WORKS = 'Изменить примеры работ'


class Balance(InlineKeyboard):
    DEPOSIT_MONEY = 'Пополнить баланс'
    WITHDRAW_MONEY = 'Вывести деньги'


class UserRoles(InlineKeyboard):
    CLIENT = 'Я заказчик'
    WORKER = 'Я исполнитель'


class Subjects(InlineKeyboard):
    CHANGE_SUBJECTS = 'Изменить предметы'

# # для поиска предметов
# find_subject = InlineKeyboard()
# find_subject.row(IButton('Найти предмет', switch_inline_query_current_chat=''))
# 
# # для предложения проекта заказчику
# choose_invite_chat = InlineKeyboard()
# choose_invite_chat.row(IButton('Выбрать чат', switch_inline_query=TextQueries.INVITE_PROJECT))
