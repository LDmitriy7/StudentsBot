from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link
from loader import calendar

find_subject = InlineKeyboardMarkup()
find_subject_btn = InlineKeyboardButton('Найти предмет', switch_inline_query_current_chat='')
find_subject.row(find_subject_btn)

work_types = InlineKeyboardMarkup(row_width=2)
work_type_btns = [
    'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая', 'Дипломная', 'Практика',
    'Эссе', 'Доклад', 'Статья', 'Тезисы', 'Презентация', 'Бизнес-план', 'Повысить уникальность'
]
work_type_inline_btns = [InlineKeyboardButton(btn, callback_data=btn) for btn in work_type_btns]
work_types.add(*work_type_inline_btns)

PICK_PROJECT_PREFIX = 'pick_project_'
GET_FILES_PREFIX = 'get_files_'


def answer_bid(bid_id: str):
    """Кнопки: позвать в чат, отказаться"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('Позвать в чат', callback_data=f'pick:bid:{bid_id}'))
    keyboard.row(InlineKeyboardButton('Отказаться', callback_data='refuse:bid'))
    return keyboard


async def project_kb(project_id: str, files=False):
    """Можно посмотреть файлы и взять проект."""
    keyboard = InlineKeyboardMarkup()
    if files:
        url = await get_start_link(GET_FILES_PREFIX + project_id)
        keyboard.row(InlineKeyboardButton('Посмотреть файлы', url=url))

    url = await get_start_link(PICK_PROJECT_PREFIX + project_id)
    keyboard.row(InlineKeyboardButton('Взять проект', url=url))
    return keyboard


def get_calendar():
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


if __name__ == '__main__':
    from aiogram.types import User

    User.set_current(User())

    print(find_subject)
    print(work_types)
    print(get_calendar())
