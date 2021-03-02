"""Набор всех обычных текстовых клавиатур."""

from aiogram.types import KeyboardButton
from aiogram.utils.keyboards import ReplyKeyboard

__all__ = [
    'back',
    'back_cancel',
    'miss',
    'miss_cancel',
    'ready',
    'ready_cancel',
    'main',
    'for_worker',
    'confirm_project',
    'phone_number',
    'phone_number_cancel',
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


back = Back()


class BackCancel(ReplyKeyboard):
    BACK = BACK
    CANCEL = CANCEL


back_cancel = BackCancel()


class Miss(ReplyKeyboard):
    MISS = MISS
    BACK = BACK


miss = Miss()


class MissCancel(ReplyKeyboard):
    MISS = MISS
    BACK = BACK
    CANCEL = CANCEL


miss_cancel = MissCancel([1])


class Ready(ReplyKeyboard):
    READY = READY
    START_OVER = START_OVER
    BACK = BACK


ready = Ready()


class ReadyCancel(ReplyKeyboard):
    READY = READY
    START_OVER = START_OVER
    BACK = BACK
    CANCEL = CANCEL


ready_cancel = ReadyCancel()


# --- частные клавиатуры ---

class Main(ReplyKeyboard):
    CREATE_POST = 'Создать пост ➕'
    PERSONAL_PROJECT = 'Личный проект 🤝'
    MY_ORDERS = 'Мои заказы 💼'
    BALANCE = 'Баланс 🤑'
    OFFER_IDEA = 'Предложить идею ✍'
    GUIDE = 'Инструкция 📑'
    WORKER_MENU = 'Меню исполнителя'


main = Main()


class ForWorker(ReplyKeyboard):
    MY_WORKS = 'Мои работы'
    SEARCH_ORDERS = 'Поиск заказов'
    MY_PROFILE = 'Мой профиль'
    MY_SUBJECTS = 'Мои предметы'
    BACK = BACK


for_worker = ForWorker()


class ConfirmProject(ReplyKeyboard):
    SEND = 'Отправить проект'
    BACK = BACK
    CANCEL = CANCEL


confirm_project = ConfirmProject([1])


class PhoneNumber(ReplyKeyboard):
    PHONE = KeyboardButton('Отправить номер', request_contact=True)
    MISS = MISS
    BACK = BACK


phone_number = PhoneNumber()


class PhoneNumberCancel(ReplyKeyboard):
    PHONE = KeyboardButton('Отправить номер', request_contact=True)
    MISS = MISS
    BACK = BACK
    CANCEL = CANCEL


phone_number_cancel = PhoneNumberCancel()

if __name__ == '__main__':
    print(back)
    print(back_cancel)
    print(miss)
    print(miss_cancel)
    print(ready)
    print(ready_cancel)
    print(main)
    print(for_worker)
    print(confirm_project)
    print(phone_number)
    print(phone_number_cancel)
