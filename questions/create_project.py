from aiogram import types
from aiogram.contrib.questions import QuestText, QuestFunc, ConvState, ConvStatesGroup

import functions as funcs
from data_types import data_classes, ProjectStatuses
from keyboards import inline_funcs, inline_plain, markup
from loader import dp, bot
from texts import templates

work_type = [
    QuestText('Это займет пару минут', markup.go_back_kb),
    QuestText('Введите тип работы:', inline_plain.work_types),
]

subject = QuestText('Отправьте название предмета', inline_plain.find_subject)


@QuestFunc
async def date():
    chat = types.Chat.get_current()
    text = 'Выберите дату сдачи'
    keyboard = inline_funcs.make_calendar()
    await bot.send_message(chat.id, text, reply_markup=keyboard)


description = QuestText(
    'Теперь опишите задание максимально подробно (только текст). Укажите время сдачи!',
    markup.go_back_kb
)

price = QuestText('Теперь введите цену (в гривнах)', markup.miss_kb)

note = QuestText('Добавьте заметку (она будет видна только вам)', markup.miss_kb)

file = QuestText(
    'Отправьте фото или файлы к работе (Загружайте фото по одному!)',
    markup.ready_kb
)


@QuestFunc
async def confirm():
    chat = types.Chat.get_current()
    udata = await dp.current_state().get_data()
    post_data = data_classes.ProjectData.from_dict(udata)

    post_text = templates.form_post_text(ProjectStatuses.ACTIVE, post_data, with_note=True)
    keyboard = markup.confirm_project_kb
    await bot.send_message(chat.id, '<b>Проверьте свой пост:</b>')
    await bot.send_message(chat.id, post_text, reply_markup=keyboard)
    await funcs.send_files(post_data.files)


# прикрепляем вопросы к состояниям
class CreateProjectConv(ConvStatesGroup):
    """Содержит все состояния создания проекта и вопросы к ним."""
    work_type = ConvState(work_type)
    subject = ConvState(subject)
    date = ConvState(date)
    description = ConvState(description)
    price = ConvState(price)
    note = ConvState(note)
    files = ConvState(file)
    confirm = ConvState(confirm)
