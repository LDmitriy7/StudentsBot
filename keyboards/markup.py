"""Набор всех обычных текстовых клавиатур."""
from aiogram.types import KeyboardButton
from data_types.keyboards import ResizedKeyboardMarkup

BACK_BTN = 'Назад'
CANCEL_BTN = 'Отменить'
_GO_BACK_BTNS = [BACK_BTN, CANCEL_BTN]

# главная клавиатура
main_kb = ResizedKeyboardMarkup()
main_kb.add(
    'Создать пост ➕', 'Личный проект 🤝', 'Мои заказы 💼', 'Баланс 🤑',
    'Предложить идею ✍', 'Инструкция 📑', 'Меню исполнителя'
)

# клавиатура для авторов
worker_kb = ResizedKeyboardMarkup()
worker_kb.add('Мои работы', 'Поиск заказов', 'Мой профиль', 'Мои предметы', BACK_BTN)

# клавиатура для отмены или шага назад
go_back_kb = ResizedKeyboardMarkup()
go_back_kb.row(*_GO_BACK_BTNS)

# клавиатура для пропуска выбора
miss_kb = ResizedKeyboardMarkup()
miss_kb.row('Пропустить')
miss_kb.row(*_GO_BACK_BTNS)

# клавиатура для окончания выбора
ready_kb = ResizedKeyboardMarkup()
ready_kb.row('Готово', 'Начать заново')
ready_kb.row(*_GO_BACK_BTNS)

# клавиатура для отмены
cancel_kb = ResizedKeyboardMarkup()
cancel_kb.row(CANCEL_BTN)

# ----- частные клавиатуры -----

# клавиатура для отправки проекта
confirm_project_kb = ResizedKeyboardMarkup()
confirm_project_kb.row('Отправить проект')
confirm_project_kb.row(*_GO_BACK_BTNS)

# клавиатура для отправки номера
phone_number = ResizedKeyboardMarkup()
phone_number.row(KeyboardButton('Отправить номер', request_contact=True), 'Пропустить')
phone_number.row(*_GO_BACK_BTNS)

# клавиатура для выбора роли в персональном проекте
# personal_project = ResizedKeyboardMarkup()
# personal_project.row('Я заказчик', 'Я исполнитель')
# personal_project.row(CANCEL_BTN)
