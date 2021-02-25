"""Набор всех обычных текстовых клавиатур."""

from aiogram.types import KeyboardButton

from data_types.keyboards import ReplyKeyboard

__all__ = [
    'Miss', 'MissCancel', 'Back', 'BackCancel', 'Ready', 'ReadyCancel', 'ForWorker',
    'ConfirmProject', 'Main', 'Back', 'PhoneNumber', 'PhoneNumberCancel',
    'BACK', 'CANCEL', 'READY', 'MISS', 'RESET', 'START_OVER'
]

BACK = 'Назад'
CANCEL = 'Отменить'
READY = 'Готово'
MISS = 'Пропустить'
RESET = 'Сбросить'
START_OVER = 'Начать заново'


# --- общие клавиатуры ---

class Back(ReplyKeyboard):
    BACK = BACK


class BackCancel(ReplyKeyboard):
    BACK = BACK
    CANCEL = CANCEL


class Miss(ReplyKeyboard):
    MISS = MISS
    BACK = BACK


class MissCancel(ReplyKeyboard):
    MISS = MISS
    BACK = BACK
    CANCEL = CANCEL

    rows_width = [1]


class Ready(ReplyKeyboard):
    READY = READY
    START_OVER = START_OVER
    BACK = BACK


class ReadyCancel(ReplyKeyboard):
    READY = READY
    START_OVER = START_OVER
    BACK = BACK
    CANCEL = CANCEL


# --- частные клавиатуры ---

class Main(ReplyKeyboard):
    CREATE_POST = 'Создать пост ➕'
    PERSONAL_PROJECT = 'Личный проект 🤝'
    MY_ORDERS = 'Мои заказы 💼'
    BALANCE = 'Баланс 🤑'
    OFFER_IDEA = 'Предложить идею ✍'
    GUIDE = 'Инструкция 📑'
    WORKER_MENU = 'Меню исполнителя'


class ForWorker(ReplyKeyboard):
    MY_WORKS = 'Мои работы'
    SEARCH_ORDERS = 'Поиск заказов'
    MY_PROFILE = 'Мой профиль'
    MY_SUBJECTS = 'Мои предметы'
    BACK = BACK


class ConfirmProject(ReplyKeyboard):
    SEND = 'Отправить проект'
    BACK = BACK
    CANCEL = CANCEL

    rows_width = [1]


class PhoneNumber(ReplyKeyboard):
    PHONE = KeyboardButton('Отправить номер', request_contact=True)
    MISS = MISS
    BACK = BACK


class PhoneNumberCancel(ReplyKeyboard):
    PHONE = KeyboardButton('Отправить номер', request_contact=True)
    MISS = MISS
    BACK = BACK
    CANCEL = CANCEL
