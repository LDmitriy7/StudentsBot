from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText

import keyboards as KB

nickname = QuestText('Введите новый никнейм', KB.back)

phone_number = QuestText('Отправьте номер телефона', KB.phone_number)

email = QuestText('Отправьте новый email', KB.miss)

biography = QuestText('Напишите о себе все, что считаете нужным', KB.back)

works = QuestText('Добавьте новые примеры работ (только фото), отправляйте фото по одному!', KB.ready)

subjects = [
    QuestText('Введите название предмета', KB.ready),
    QuestText('Вы можете использовать поиск', KB.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
