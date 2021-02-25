from aiogram.contrib.questions import ConvState, ConvStatesGroup, QuestText

from keyboards import markup
import keyboards as KB

nickname = QuestText('Придумайте себе никнейм', KB.Back)

phone_number = QuestText('Отправьте номер телефона', KB.PhoneNumber)

email = QuestText('Отправьте email', KB.Miss)

biography = QuestText('Напишите о себе все, что считаете нужным', KB.Back)

works = QuestText(
    'Отправьте примеры ваших работ (только фото), отправляйте фото по одному!',
    KB.Ready,
)


# прикрепляем вопросы к состояниям
class RegistrationConv(ConvStatesGroup):
    """Содержит все состояния для регистрации и вопросы к ним."""
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
