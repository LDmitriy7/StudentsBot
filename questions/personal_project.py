from aiogram import types

from keyboards import inline_kb, markup
from loader import dp
from questions.misc import ConvState, ConvStatesGroup, QuestFunc, QuestText
from texts import templates

work_type = [
    QuestText('Это займет пару минут', markup.go_back_kb),
    QuestText('Введите тип работы:', inline_kb.work_types),
]

subject = QuestText('Отправьте название предмета', inline_kb.find_subject)


@QuestFunc
async def date(msg: types.Message):
    text = 'Выберите дату сдачи'
    keyboard = inline_kb.get_calendar()
    await msg.answer(text, reply_markup=keyboard)


description = QuestText(
    'Теперь опишите задание максимально подробно (только текст). Укажите время сдачи!',
    markup.go_back_kb
)

price = QuestText('Теперь введите цену (в гривнах)', markup.miss_kb)

note = QuestText('Добавьте заметку (она будет видна только вам)', markup.miss_kb)

file = QuestText(
    'Отправьте фото или файл к работе (Загружайте фото по одному!)',
    markup.ready_kb
)

worker = QuestText('Введите ID исполнителя', markup.go_back_kb)


@QuestFunc
async def confirm(msg: types.Message):
    post_data = await dp.current_state().get_data()
    text1 = 'Проверьте свой пост:'
    post_text = templates.form_post_text(post_data)
    keyboard = markup.confirm_kb
    await msg.answer(text1)
    await msg.answer(post_text, reply_markup=keyboard)


class PersonalProject(ConvStatesGroup):
    work_type = ConvState(work_type)
    subject = ConvState(subject)
    date = ConvState(date)
    description = ConvState(description)
    price = ConvState(price)
    note = ConvState(note)
    file = ConvState(file)
    worker = ConvState(worker)
    confirm = ConvState(confirm)
