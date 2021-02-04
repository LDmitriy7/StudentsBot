"""Imports all handlers sets.
1) common (special) handlers must be at the top
2) balance should be closer to the top (for guaranteed deposits)
3) errors must be at the end.
"""

from handlers import common  # команды "Отменить", "Назад" ; Удаление сообщения
from handlers import search_subjects  # инлайн-поиск предметов +
from handlers import projects  # обработка кнопок под проектом: посмотреть файлы, взять проект, удалить проект
from handlers import registration  # вся для диалога: регистрация профиля и страницы исполнителя +

from handlers import bids

from handlers import main_menu
from handlers import worker_menu  # обработка команд с клавиатуры исполнителя +

from handlers import errors  # подавление некоторых ошибок и предупредительное сообщение
