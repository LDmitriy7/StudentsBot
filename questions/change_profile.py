from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText

from keyboards import markup, inline_plain
from keyboards.markup import BackKeyboard, MissKeyboard

nickname = QuestText('Введите новый никнейм', BackKeyboard(BACK=None))

phone_number = QuestText('Отправьте номер телефона', markup.phone_number(back_btn=False))

email = QuestText('Отправьте новый email', MissKeyboard(BACK=None))

biography = QuestText('Напишите о себе все, что считаете нужным', BackKeyboard(BACK=None))

works = QuestText(
    'Добавьте новые примеры работ (только фото), отправляйте фото по одному!',
    markup.ReadyKeyboard(BACK=None),
)

subjects = [
    QuestText('Введите название предмета', markup.ReadyKeyboard(BACK=None)),
    QuestText('Вы можете использовать поиск', inline_plain.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
