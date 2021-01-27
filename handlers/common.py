from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import markup, inline_func
from questions import ALL_CONV_STATES_GROUPS, ALL_CONV_STATES, ConvStatesGroup
from questions.misc import HandleException, ConvState, ask_question


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
            await _ask_previous(msg, state, states_group)
            break
    else:
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)

    return HandleException()  # exception in any case


@dp.callback_query_handler(text=inline_func.DEL_MESSAGE_DATA)
async def delete_msg(query: types.CallbackQuery):
    await query.message.delete()


async def _ask_previous(msg: types.Message, state: FSMContext, states_group: ConvStatesGroup):
    new_state_name = await states_group.previous()

    if new_state_name is None:  # user has left conversation
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    else:
        new_state: ConvState = ALL_CONV_STATES[new_state_name]
        await ask_question(msg, new_state.question)
