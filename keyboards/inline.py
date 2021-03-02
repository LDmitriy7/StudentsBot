from aiogram.utils.keyboards import InlineKeyboard, Buttons
from config import MONOBANK_PAYMENT_URL, PRIVAT_BANK_PAYMENT_url

__all__ = [
    'rates',
    'work_types',
    'my_profile',
    'balance',
    'user_roles',
    'subjects',
    'find_subject',
    'choose_invite_chat',
    'payment',
]


class Payment(InlineKeyboard):
    MONOBANK = Buttons.url('Монобанк', MONOBANK_PAYMENT_URL)
    PRIVATBANK = Buttons.url('Приватбанк', PRIVAT_BANK_PAYMENT_url)
    ASK_CONFIRM = 'Подтвердить оплату'


payment = Payment()


class Rates(InlineKeyboard):
    BUTTONS = ['1 ☆', '2 ☆', '3 ☆', '4 ☆', '5 ☆']


rates = Rates(default_width=5)


class WorkTypes(InlineKeyboard):
    BUTTONS = [
        'Онлайн помощь', 'Домашняя работа', 'Лабораторная', 'Реферат', 'Курсовая',
        'Дипломная', 'Практика', 'Эссе', 'Доклад', 'Статья', 'Тезисы',
        'Презентация', 'Бизнес-план', 'Повысить уникальность'
    ]


work_types = WorkTypes(default_width=2)


class MyProfile(InlineKeyboard):
    CHANGE_NICKNAME = 'Изменить никнейм'
    CHANGE_PHONE_NUMBER = 'Изменить телефон'
    CHANGE_EMAIL = 'Изменить email'
    CHANGE_BIOGRAPHY = 'Изменить биографию'
    CHANGE_WORKS = 'Изменить примеры работ'


my_profile = MyProfile()


class Balance(InlineKeyboard):
    DEPOSIT_MONEY = 'Пополнить баланс'
    WITHDRAW_MONEY = 'Вывести деньги'


balance = Balance()


class UserRoles(InlineKeyboard):
    CLIENT = 'Я заказчик'
    WORKER = 'Я исполнитель'


user_roles = UserRoles()


class Subjects(InlineKeyboard):
    CHANGE = 'Изменить предметы'


subjects = Subjects()


class FindSubject(InlineKeyboard):
    FIND_QUERY = Buttons.switch_iquery_current('Найти предмет', '')


find_subject = FindSubject()


class ChooseInviteChat(InlineKeyboard):
    INVITE_QUERY = Buttons.switch_iquery('Выбрать чат', 'Предложить проект')


choose_invite_chat = ChooseInviteChat()

if __name__ == '__main__':
    print(rates)
    print(work_types)
    print(my_profile)
    print(balance)
    print(user_roles)
    print(subjects)
    print(find_subject)
    print(choose_invite_chat)