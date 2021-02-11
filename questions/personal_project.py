from aiogram import types

import functions.files
from functions import common as cfuncs
from keyboards import inline_funcs, inline_plain, markup
from loader import dp
from questions.misc import ConvState, ConvStatesGroup, QuestFunc, QuestText
from texts import templates

work_type = [
    QuestText('Это займет пару минут', markup.go_back_kb),
    QuestText('Введите тип работы:', inline_plain.work_types),
]

subject = QuestText('Отправьте название предмета', inline_plain.find_subject)


@QuestFunc
async def date(msg: types.Message):
    text = 'Выберите дату сдачи'
    keyboard = inline_funcs.make_calendar()
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


# worker = QuestText('Введите ID исполнителя', markup.go_back_kb)


@QuestFunc
async def confirm(msg: types.Message):
    post_data = await dp.current_state().get_data()
    files = post_data.get('files', [])

    post_text = templates.form_post_text('Активен', post_data, with_note=True)
    keyboard = markup.confirm_project_kb
    await msg.answer('<b>Проверьте свой пост:</b>', reply_markup=keyboard)
    await msg.answer(post_text)

    if files:
        await msg.answer('<b>Файлы к проекту:</b>')
        for file in files:
            await functions.files.send_file(msg.from_user.id, *file)


# прикрепляем вопросы к состояниям
class PersonalProjectConv(ConvStatesGroup):
    work_type = ConvState(work_type)
    subject = ConvState(subject)
    date = ConvState(date)
    description = ConvState(description)
    price = ConvState(price)
    note = ConvState(note)
    files = ConvState(file)
    # worker = ConvState(worker)
    confirm = ConvState(confirm)
