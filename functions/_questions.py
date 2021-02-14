from ques


async def ask_prev_question(msg: types.Message, state: FSMContext, states_group: ConvStatesGroup):
    new_state_name = await states_group.previous()

    if new_state_name is None:  # user has left conversation
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    else:
        new_state: ConvState = ALL_CONV_STATES[new_state_name]
        await ask_question(msg, new_state.question)
