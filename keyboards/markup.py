"""Набор всех обычных текстовых клавиатур."""
from aiogram.types import KeyboardButton

from data_types.keyboards import ResizedKeyboardMarkup, make_keyboard


class Buttons:
    BACK = 'Назад'
    CANCEL = 'Отменить'
    READY = 'Готово'
    MISS = 'Пропустить'
    RESET = 'Сбросить'
    START_OVER = 'Начать заново'
    GO_BACK = [BACK, CANCEL]


# главная клавиатура
main_kb = ResizedKeyboardMarkup()
main_kb.add(
    'Создать пост ➕', 'Личный проект 🤝', 'Мои заказы 💼', 'Баланс 🤑',
    'Предложить идею ✍', 'Инструкция 📑', 'Меню исполнителя'
)

# клавиатура для авторов
worker_kb = ResizedKeyboardMarkup()
worker_kb.add('Мои работы', 'Поиск заказов', 'Мой профиль', 'Мои предметы', Buttons.BACK)


def go_back_kb(back_btn=True, cancel_btn=True):
    btns = {Buttons.BACK: back_btn, Buttons.CANCEL: cancel_btn}
    return make_keyboard(btns)


def miss_kb(miss_btn=True, back_btn=True, cancel_btn=True):
    """Клавиатура для пропуска выбора"""
    btns = {Buttons.MISS: miss_btn}, {Buttons.BACK: back_btn, Buttons.CANCEL: cancel_btn}
    return make_keyboard(*btns)


def ready_kb(ready_btn=True, start_over_btn=True, back_btn=True, cancel_btn=True):
    row = {Buttons.READY: ready_btn, Buttons.START_OVER: start_over_btn}
    row2 = {Buttons.BACK: back_btn, Buttons.CANCEL: cancel_btn}
    return make_keyboard(row, row2)


# --- частные клавиатуры ---

# клавиатура для отправки проекта
confirm_project_kb = ResizedKeyboardMarkup()
confirm_project_kb.row('Отправить проект')
confirm_project_kb.row(*Buttons.GO_BACK)


# клавиатура для отправки номера
def phone_number(miss_btn=True, back_btn=True, cancel_btn=True):
    row = {KeyboardButton('Отправить номер', request_contact=True): True, Buttons.MISS: miss_btn}
    row2 = {Buttons.BACK: back_btn, Buttons.CANCEL: cancel_btn}
    return make_keyboard(row, row2)
