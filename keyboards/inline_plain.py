"""Простые инлайновые клавиатуры."""
from typing import List

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.helper import Helper, Item


def _get_same_inline_button(buttons: List[str]):
    """Создает инлайн-кнопки из обычных, где [callback_data = text]"""
    return [Button(btn, callback_data=btn) for btn in buttons]


class InlineKeyboard(InlineKeyboardMarkup, Helper):
    def add_row(self, text: str, callback_data: str):
        self.row(Button(text, callback_data=callback_data))


class WorkTypeKeyboard(InlineKeyboard):
    WORK_TYPE_BTNS = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая', 'Дипломная', 'Практика',
        'Эссе', 'Доклад', 'Статья', 'Тезисы', 'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]
    WORK_TYPE_INLINE_BTNS = _get_same_inline_button(WORK_TYPE_BTNS)


class MyProfileKeyboard(InlineKeyboard):
    CHANGE_NICKNAME = Item()
    CHANGE_PHONE_NUMBER = Item()
    CHANGE_EMAIL = Item()
    CHANGE_BIOGRAPHY = Item()
    CHANGE_WORKS = Item()


class BalanceKeyboard(InlineKeyboard):
    DEPOSIT_MONEY = Item()
    WITHDRAW_MONEY = Item()


class SubjectsKeyboard(InlineKeyboard):
    CHANGE_SUBJECTS = Item()


# для поиска предметов
find_subject = InlineKeyboard()
find_subject.row(Button('Найти предмет', switch_inline_query_current_chat=''))

# для выбора типа работы
work_types = WorkTypeKeyboard(row_width=2)
work_types.add(*work_types.WORK_TYPE_INLINE_BTNS)

# для пополнения баланса и вывода
balance = BalanceKeyboard()
balance.add_row('Пополнить баланс', balance.DEPOSIT_MONEY)
balance.add_row('Вывести деньги', balance.WITHDRAW_MONEY)

# для изменения предметов
subjects = SubjectsKeyboard()
subjects.add_row('Изменить предметы', subjects.CHANGE_SUBJECTS)

# для изменения профиля
change_profile = MyProfileKeyboard()
change_profile.add_row('Изменить никнейм', change_profile.CHANGE_NICKNAME)
change_profile.add_row('Изменить телефон', change_profile.CHANGE_PHONE_NUMBER)
change_profile.add_row('Изменить email', change_profile.CHANGE_EMAIL)
change_profile.add_row('Изменить биографию', change_profile.CHANGE_BIOGRAPHY)
change_profile.add_row('Изменить примеры работ', change_profile.CHANGE_WORKS)
