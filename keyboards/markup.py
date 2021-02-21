"""Набор всех обычных текстовых клавиатур."""
from dataclasses import dataclass
from typing import Optional

from aiogram.types import KeyboardButton

from data_types.keyboards import ResizedKeyboard, make_keyboard

__all__ = ['Miss', 'Ready', 'ForWorker', 'ConfirmProject', 'Main', 'Back', 'phone_number']

_B = Optional[str]


class CButtons:
    BACK = 'Назад'
    CANCEL = 'Отменить'
    READY = 'Готово'
    MISS = 'Пропустить'
    RESET = 'Сбросить'
    START_OVER = 'Начать заново'


# --- общие клавиатуры ---

@dataclass
class Back(ResizedKeyboard):
    BACK: _B = CButtons.BACK
    CANCEL: _B = CButtons.CANCEL


@dataclass
class Miss(ResizedKeyboard):
    MISS: _B = CButtons.MISS
    BACK: _B = CButtons.BACK
    CANCEL: _B = CButtons.CANCEL


@dataclass
class Ready(ResizedKeyboard):
    READY: _B = CButtons.READY
    START_OVER: _B = CButtons.START_OVER
    BACK: _B = CButtons.BACK
    CANCEL: _B = CButtons.CANCEL


# --- частные клавиатуры ---

@dataclass
class Main(ResizedKeyboard):
    CREATE_POST: _B = 'Создать пост ➕'
    PERSONAL_PROJECT: _B = 'Личный проект 🤝'
    MY_ORDERS: _B = 'Мои заказы 💼'
    BALANCE: _B = 'Баланс 🤑'
    OFFER_IDEA: _B = 'Предложить идею ✍'
    GUIDE: _B = 'Инструкция 📑'
    WORKER_MENU: _B = 'Меню исполнителя'


@dataclass
class ForWorker(ResizedKeyboard):
    MY_WORKS: _B = 'Мои работы'
    SEARCH_ORDERS: _B = 'Поиск заказов'
    MY_PROFILE: _B = 'Мой профиль'
    MY_SUBJECTS: _B = 'Мои предметы'
    BACK: _B = CButtons.BACK


@dataclass
class ConfirmProject(ResizedKeyboard):
    SEND: _B = 'Отправить проект'
    BACK: _B = CButtons.BACK
    CANCEL: _B = CButtons.CANCEL


# клавиатура для отправки номера
def phone_number(miss_btn=True, back_btn=True, cancel_btn=True):
    row = {KeyboardButton('Отправить номер', request_contact=True): True, CButtons.MISS: miss_btn}
    row2 = {CButtons.BACK: back_btn, CButtons.CANCEL: cancel_btn}
    return make_keyboard(row, row2)
