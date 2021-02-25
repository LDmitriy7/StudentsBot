from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText

import keyboards as KB
from keyboards import markup, inline_plain

nickname = QuestText('Введите новый никнейм', KB.Back)

phone_number = QuestText('Отправьте номер телефона', KB.PhoneNumber)

email = QuestText('Отправьте новый email', KB.Miss)

biography = QuestText('Напишите о себе все, что считаете нужным', KB.Back)

works = QuestText(
    'Добавьте новые примеры работ (только фото), отправляйте фото по одному!',
    markup.Ready,
)

subjects = [
    QuestText('Введите название предмета', KB.Ready),
    QuestText('Вы можете использовать поиск', inline_plain.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
