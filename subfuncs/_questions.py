from aiogram.dispatcher.filters.state import State, StatesGroup, StatesGroupMeta
from typing import Optional


#
# async def ask_prev_question(msg: types.Message, state: FSMContext, states_group: StatesGroup):
#     new_state_name = await states_group.previous()
#
#     if new_state_name is None:  # user has left conversation
#         await state.finish()
#         await msg.answer('Отменено', reply_markup=markup.MainKeyboard())
#     else:
#         new_state: ConvState = ALL_CONV_STATES[new_state_name]
#         await ask_question(msg, new_state.question)


def get_state_by_name(state_name: str, base_states_group: StatesGroupMeta = StatesGroup):
    """Search for State with state_name in subclasses of base_states_group."""
    for state_group in base_states_group.__subclasses__():
        for state in state_group.states:
            if state.state == state_name:
                return state
