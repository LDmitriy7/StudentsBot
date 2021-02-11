"""Handle commands "Отменить", "Назад" and query for deleting bound message."""
from aiogram import types
from aiogram.dispatcher import FSMContext

import questions.misc
from functions import common as cfuncs
from keyboards import inline_funcs, markup
from loader import dp
from questions import ALL_CONV_STATES_GROUPS
from questions.misc import HandleException
from texts import main as texts


@dp.message_handler(text='/start')
async def send_welcome(msg: types.Message):
    await msg.answer(texts.welcome, reply_markup=markup.main_kb)


@dp.message_handler(text='Отменить', state='*')
@dp.message_handler(commands='cancel', state='*')
async def cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('Отменено', reply_markup=markup.main_kb)


@dp.message_handler(text='Назад', state='*')
@dp.message_handler(commands='back', state='*')
async def go_back(msg: types.Message, state: FSMContext):
    state_name = await state.get_state()

    for states_group, all_states_names in ALL_CONV_STATES_GROUPS.items():
        if state_name in all_states_names:  # user is in conversation
            await questions.misc.ask_prev_question(msg, state, states_group)
            break
    else:
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    return HandleException()  # exception in any case


@dp.callback_query_handler(text=inline_funcs.DEL_MESSAGE_DATA)
async def delete_msg(query: types.CallbackQuery):
    await query.message.delete()
