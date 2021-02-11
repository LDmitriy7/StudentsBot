"""Contain all questions (ConvStatesGroups with question for each state)."""

from questions import create_post, personal_project, registration
from questions.misc import ConvStatesGroup, ConvState, ask_question
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards import markup

ConvSubClasses = ConvStatesGroup.__subclasses__()

ALL_CONV_STATES_GROUPS = {sg: sg.all_states_names for sg in ConvSubClasses}
ALL_CONV_STATES = {state.state: state for sg in ConvSubClasses for state in sg.all_states}


async def ask_prev_question(msg: types.Message, state: FSMContext, states_group: ConvStatesGroup):
    new_state_name = await states_group.previous()

    if new_state_name is None:  # user has left conversation
        await state.finish()
        await msg.answer('Отменено', reply_markup=markup.main_kb)
    else:
        new_state: ConvState = ALL_CONV_STATES[new_state_name]
        await ask_question(msg, new_state.question)
