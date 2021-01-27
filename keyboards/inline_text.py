"""Простые инлайновые клавиатуры."""
from aiogram.types import InlineKeyboardMarkup as InlineKeyboard
from aiogram.types import InlineKeyboardButton as InlineButton
from typing import List
from aiogram.utils.helper import Item, Helper


def get_same_inline_button(buttons: List[str]):
    """Создает инлайн-кнопки из обычных, где [callback_data = text]"""
    return [InlineButton(btn, callback_data=btn) for btn in buttons]


class WorkTypeKeyboard(InlineKeyboard):
    WORK_TYPE_BTNS = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая', 'Дипломная', 'Практика',
        'Эссе', 'Доклад', 'Статья', 'Тезисы', 'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]
    WORK_TYPE_INLINE_BTNS = get_same_inline_button(WORK_TYPE_BTNS)


class BalanceKeyboard(InlineKeyboard, Helper):
    DEPOSIT_MONEY = Item()
    WITHDRAW_MONEY = Item()


class SubjectsKeyboard(InlineKeyboard, Helper):
    CHANGE_SUBJECTS = Item()


# для поиска предметов
find_subject = InlineKeyboard()
find_subject.row(InlineButton('Найти предмет', switch_inline_query_current_chat=''))

# для выбора типа работы
work_types = WorkTypeKeyboard(row_width=2)
work_types.add(*WorkTypeKeyboard.WORK_TYPE_INLINE_BTNS)

# для пополнения баланса и вывода
balance = BalanceKeyboard()
balance.row(InlineButton('Пополнить баланс', callback_data=BalanceKeyboard.DEPOSIT_MONEY))
balance.row(InlineButton('Вывести деньги', callback_data=BalanceKeyboard.WITHDRAW_MONEY))

# для изменения предметов
subjects = SubjectsKeyboard()
subjects.row(InlineButton('Изменить предметы', callback_data=SubjectsKeyboard.CHANGE_SUBJECTS))

if __name__ == '__main__':
    print(balance)
    print(work_types)
    print(subjects)
