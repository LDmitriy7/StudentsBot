from keyboards import markup
from questions.misc import ConvState, ConvStatesGroup, QuestText

nickname = QuestText('Придумайте себе никнейм', markup.go_back_kb)

phone_number = QuestText('Отправьте номер телефона', markup.phone_number)

email = QuestText('Отправьте email', markup.miss_kb)

biography = QuestText('Напишите о себе все, что считаете нужным', markup.miss_kb)

works = QuestText(
    'Отправьте примеры ваших работ (фото или документы), отправляйте фото по одному!',
    markup.ready_kb,
)


# прикрепляем вопросы к состояниям
class RegistrationConv(ConvStatesGroup):
    """Содержит все состояния для регистрации и вопросы к ним."""
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)