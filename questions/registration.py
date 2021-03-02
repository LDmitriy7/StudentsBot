from aiogram.contrib.questions import ConvState, ConvStatesGroup, QuestText

import keyboards as KB

nickname = QuestText('Придумайте себе никнейм', KB.back_cancel)

phone_number = QuestText('Отправьте номер телефона', KB.phone_number_cancel)

email = QuestText('Отправьте email', KB.miss_cancel)

biography = QuestText('Напишите о себе все, что считаете нужным', KB.back_cancel)

works = QuestText('Отправьте примеры ваших работ (только фото), отправляйте фото по одному!', KB.ready_cancel)


class RegistrationConv(ConvStatesGroup):
    """Содержит все состояния для регистрации и вопросы к ним."""
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
