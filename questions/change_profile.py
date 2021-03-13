from aiogram.contrib.questions import ConvState, SingleConvStatesGroup, QuestText, QuestFunc
from aiogram import html
import keyboards as KB

nickname = QuestText('Введите новый никнейм', KB.back)

phone_number = QuestText(
    'Отправьте номер телефона, нажав на кнопку, или введите его самостоятельно (только цифры)',
    KB.phone_number
)

email = QuestText('Отправьте новый email', KB.back)

biography = QuestText('Напишите о себе все, что считаете нужным', KB.back)

works = QuestText('Добавьте новые примеры работ (только фото), отправляйте фото по одному!', KB.ready)

subjects = [
    QuestText('Выберите категорию предметов', KB.ready),
    QuestText(html.b('Все категории:'), KB.subjects_categories)
]

subjects_manually = [
    QuestText('Введите название предмета, чтобы добавить или удалить его', KB.ready),
    QuestText('Вы можете использовать инлайн-поиск', KB.find_subject)
]


class ChangeProfile(SingleConvStatesGroup):
    phone_number = ConvState(phone_number)
    email = ConvState(email)
    biography = ConvState(biography)
    works = ConvState(works)
    nickname = ConvState(nickname)
    subjects = ConvState(subjects)
    subjects_manually = ConvState(subjects_manually)
