"""Contain all questions (ConvStatesGroups with question for each state)."""

from questions.create_project import CreateProjectConv
from questions.registration import RegistrationConv

# from aiogram.dispatcher.filters.state import State
# from data_types.for_quests import ConvStatesGroup
# ConvSubClasses: list[type[ConvStatesGroup]] = ConvStatesGroup.__subclasses__()
#
# ALL_CONV_STATES: dict[str, State] = {
#     state.state: state for sg in ConvSubClasses for state in sg.all_states
# }
#
# ALL_CONV_STATES_GROUPS: dict[type[ConvStatesGroup], list[str]] = {
#     sg: sg.all_states_names for sg in ConvSubClasses
# }
