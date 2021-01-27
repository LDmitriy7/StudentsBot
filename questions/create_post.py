from aiogram import types

from keyboards import inline_func, inline_text, markup
from loader import dp
from questions.misc import ConvState, ConvStatesGroup, QuestFunc, QuestText
from texts import templates

work_type = [
    QuestText('Это займет пару минут', markup.go_back_kb),
    QuestText('Введите тип работы:', inline_text.work_types),
]

subject = QuestText('Отправьте название предмета', inline_text.find_subject)


@QuestFunc
async def date(msg: types.Message):
    text = 'Выберите дату сдачи'
    keyboard = inline_func.get_calendar()
    await msg.answer(text, reply_markup=keyboard)


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
async def confirm(msg: types.Message):
    post_data = await dp.current_state().get_data()
    status = post_data['status']
    post_text = templates.form_post_text(status, post_data, with_note=True)
    keyboard = markup.confirm_project_kb
    await msg.answer('Проверьте свой пост:', reply_markup=keyboard)
    await msg.answer(post_text)


# прикрепляем вопросы к состояниям
class CreatePostConv(ConvStatesGroup):
    """Содержит все состояния создания поста и вопросы к ним."""
    work_type = ConvState(work_type)
    subject = ConvState(subject)
    date = ConvState(date)
    description = ConvState(description)
    price = ConvState(price)
    note = ConvState(note)
    files = ConvState(file)
    confirm = ConvState(confirm)
