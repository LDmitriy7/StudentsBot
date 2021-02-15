"""Handle commands "Отменить", "Назад" and query for deleting bound message."""
from aiogram import types
from aiogram.dispatcher import FSMContext

import questions.misc
from keyboards import inline_funcs, markup
from loader import dp
from questions import ALL_CONV_STATES_GROUPS
from datatypes import HandleException
from texts import main as texts


@dp.message_handler(text='/start', state='*', chat_type='private')
async def send_welcome(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(texts.welcome, reply_markup=markup.main_kb)


@dp.message_handler(text='Отменить', state='*')
@dp.message_handler(commands='cancel', state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    keyboard = markup.main_kb if msg.chat.type == 'private' else None
    await msg.answer('Отменено', reply_markup=keyboard)


@dp.message_handler(text='Назад', state='*')
@dp.message_handler(commands='back', state='*')
async def go_back(msg: types.Message, state: FSMContext):
    st_name = await state.get_state()

    for st_group, all_st_names in ALL_CONV_STATES_GROUPS.items():
        if st_name in all_st_names:  # user is in conversation
            await questions.ask_prev_question(msg, state, st_group)
            break
    else:
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    return HandleException()  # exception in any case


@dp.callback_query_handler(text=inline_funcs.DEL_MESSAGE_DATA)
async def delete_msg(query: types.CallbackQuery):
    await query.message.delete()
