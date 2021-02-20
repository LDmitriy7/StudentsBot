from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText

from keyboards import markup, inline_plain

nickname = QuestText('Введите новый никнейм', markup.go_back_kb(back_btn=False))

phone_number = QuestText('Отправьте номер телефона', markup.phone_number(back_btn=False))

email = QuestText('Отправьте новый email', markup.miss_kb(back_btn=False))

biography = QuestText('Напишите о себе все, что считаете нужным', markup.go_back_kb(back_btn=False))

works = QuestText(
    'Добавьте новые примеры работ (только фото), отправляйте фото по одному!',
    markup.ready_kb(back_btn=False),
)

subjects = [
    QuestText('Введите название предмета', markup.ready_kb(back_btn=False)),
    QuestText('Вы можете использовать поиск', inline_plain.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
