from aiogram.types import ReplyKeyboardMarkup


class ResizedKeyboardMarkup(ReplyKeyboardMarkup):
    """ReplyKeyboardMarkup with [resize_keyboard=True, row_width=2]"""

    def __init__(self, row_width: int = 2):
        super().__init__(resize_keyboard=True, row_width=row_width)

    def __repr__(self):
        return super().__str__()


GO_BACK_BTNS = 'Назад', 'Отменить'

main_kb = ResizedKeyboardMarkup()
main_kb_buttons = [
    'Создать пост ➕', 'Личный проект 🤝', 'Мои работы 🛠', 'Мои заказы 💼', 'Мое резюме 🎓',
    'Мой рейтинг ⭐', 'Баланс 🤑', 'Инструкция 📑', 'Получить помощь ✍'
]
main_kb.add(*main_kb_buttons)

go_back_kb = ResizedKeyboardMarkup()
go_back_kb.row(*GO_BACK_BTNS)

miss_kb = ResizedKeyboardMarkup()
miss_kb.row('Пропустить')
miss_kb.row(*GO_BACK_BTNS)

ready_kb = ResizedKeyboardMarkup()
ready_kb.row('Готово', 'Сбросить выбор')
ready_kb.row(*GO_BACK_BTNS)

confirm_project_kb = ResizedKeyboardMarkup()
confirm_project_kb.row('Отправить проект')
confirm_project_kb.row(*GO_BACK_BTNS)

cancel_kb = ResizedKeyboardMarkup()
cancel_kb.row('Отменить')

if __name__ == '__main__':
    print(go_back_kb)
    print(miss_kb)
    print(ready_kb)
    print(confirm_project_kb)
