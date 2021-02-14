"""Contain all questions (ConvStatesGroups with question for each state)."""

from aiogram.dispatcher.filters.state import State

from questions.create_project import CreateProjectConv
from questions.misc import ConvStatesGroup, ConvState, ask_question
from questions.registration import RegistrationConv

__all__ = [
    'ALL_CONV_STATES', 'ALL_CONV_STATES_GROUPS', 'CreateProjectConv', 'RegistrationConv'
]

ConvSubClasses: list[type[ConvStatesGroup]] = ConvStatesGroup.__subclasses__()

ALL_CONV_STATES: dict[str, State] = {
    state.state: state for sg in ConvSubClasses for state in sg.all_states
}

ALL_CONV_STATES_GROUPS: dict[type[ConvStatesGroup], list[str]] = {
    sg: sg.all_states_names for sg in ConvSubClasses
}
