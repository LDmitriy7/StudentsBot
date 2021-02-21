from aiogram.contrib.questions import ConvState, ConvStatesGroup, QuestText

from keyboards import markup
from keyboards.markup import BackKeyboard, MissKeyboard

nickname = QuestText('Придумайте себе никнейм', BackKeyboard())

phone_number = QuestText('Отправьте номер телефона', markup.phone_number())

email = QuestText('Отправьте email', MissKeyboard())

biography = QuestText('Напишите о себе все, что считаете нужным', BackKeyboard())

works = QuestText(
    'Отправьте примеры ваших работ (только фото), отправляйте фото по одному!',
    markup.ReadyKeyboard(),
)


# прикрепляем вопросы к состояниям
class RegistrationConv(ConvStatesGroup):
    """Содержит все состояния для регистрации и вопросы к ним."""
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
