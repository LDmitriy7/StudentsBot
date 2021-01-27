"""Набор всех обычных текстовых клавиатур."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ResizedKeyboardMarkup(ReplyKeyboardMarkup):
    """ReplyKeyboardMarkup with [resize_keyboard=True, row_width=2]"""

    def __init__(self, row_width: int = 2):
        super().__init__(resize_keyboard=True, row_width=row_width)

    def __repr__(self):
        return super().__str__()

    def __contains__(self, item):
        buttons = []
        for row in self.keyboard:
            buttons.extend(row)
        return item in buttons


_GO_BACK_BTNS = ['Назад', 'Отменить']

# главная клавиатура
main_kb = ResizedKeyboardMarkup()
main_kb.add(
    'Создать пост ➕', 'Личный проект 🤝', 'Мои заказы 💼', 'Баланс 🤑',
    'Предложить идею ✍', 'Инструкция 📑', 'Меню исполнителя'
)

# клавиатура для авторов
worker_kb = ResizedKeyboardMarkup()
worker_kb.add('Мои работы', 'Мои заявки', 'Поиск заказов', 'Мой профиль', 'Мои предметы', 'Назад')

# клавиатура для отмены или шага назад
go_back_kb = ResizedKeyboardMarkup()
go_back_kb.row(*_GO_BACK_BTNS)

# клавиатура для пропуска выбора
miss_kb = ResizedKeyboardMarkup()
miss_kb.row('Пропустить')
miss_kb.row(*_GO_BACK_BTNS)

# клавиатура для окончания выбора
ready_kb = ResizedKeyboardMarkup()
ready_kb.row('Готово', 'Сбросить выбор')
ready_kb.row(*_GO_BACK_BTNS)

# клавиатура для отмены
cancel_kb = ResizedKeyboardMarkup()
cancel_kb.row('Отменить')

# ----- частные клавиатуры -----

# клавиатура для отправки проекта
confirm_project_kb = ResizedKeyboardMarkup()
confirm_project_kb.row('Отправить проект')
confirm_project_kb.row(*_GO_BACK_BTNS)

# клавиатура для отправки номера
phone_number = ResizedKeyboardMarkup()
phone_number.row(KeyboardButton('Отправить номер', request_contact=True), 'Пропустить')
phone_number.row(*_GO_BACK_BTNS)

if __name__ == '__main__':
    print(main_kb.keyboard)
    print('Сбросить выбор' in ready_kb)
