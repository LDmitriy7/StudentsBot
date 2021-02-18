"""Imports all group_handlers sets.
1) common (special) group_handlers must be at the top
2) balance should be closer to the top (for guaranteed deposits)
3) errors must be at the end.
"""

from handlers import common  # команды "Отменить", "Назад", удаление сообщения +

# from handlers import invite_project  # приглашение клиента заполнить проект +
# from handlers import offer_project  # инлайн отправка и принятие личного проекта +
from handlers import search_subjects  # инлайн-поиск предметов ++

from handlers import main_menu  # обработка команд с главной клавиатуры

"""
from handlers import worker_menu  # обработка команд с клавиатуры исполнителя +
from handlers import group_handlers

from handlers import bids  # отправка и принятие заявки на проект +
from handlers import projects  # обработка кнопок для проекта: посмотреть файлы, удалить проект +

"""

from handlers import registration  # все для диалога: регистрация профиля и страницы исполнителя +
from handlers import errors  # подавление некоторых ошибок и предупредительное сообщение +
