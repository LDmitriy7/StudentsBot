"""Хендлеры для команд с кнопок главного меню"""

from handlers.main_menu import create_project  # полностью отвечает за создание поста ++
from handlers.main_menu import entry_create_project  # вход в создание проекта ++
from handlers.main_menu import my_orders  # отвечает за кнопку "Мои заказы", показывает весь список ++
from handlers.main_menu import other  # кнопки 'Предложить идею', 'Инструкция' и 'Меню исполнителя' ++
from handlers.main_menu import send_project  # отправка проекта в канал/лично/самостоятельно ++

# from handlers.main_menu import _balance  # изменить
