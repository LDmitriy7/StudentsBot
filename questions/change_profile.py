from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText

from keyboards import markup, inline_plain
from keyboards.markup import Back, Miss

nickname = QuestText('Введите новый никнейм', Back(BACK=None))

phone_number = QuestText('Отправьте номер телефона', markup.phone_number(back_btn=False))

email = QuestText('Отправьте новый email', Miss(BACK=None))

biography = QuestText('Напишите о себе все, что считаете нужным', Back(BACK=None))

works = QuestText(
    'Добавьте новые примеры работ (только фото), отправляйте фото по одному!',
    markup.Ready(BACK=None),
)

subjects = [
    QuestText('Введите название предмета', markup.Ready(BACK=None)),
    QuestText('Вы можете использовать поиск', inline_plain.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
