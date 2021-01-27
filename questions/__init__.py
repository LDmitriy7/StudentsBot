"""Contain all questions (ConvStatesGroups with question for each state)."""

from questions import create_post, personal_project, registration
from questions.misc import ConvStatesGroup

ConvSubClasses = ConvStatesGroup.__subclasses__()

ALL_CONV_STATES_GROUPS = {sg: sg.all_states_names for sg in ConvSubClasses}
ALL_CONV_STATES = {state.state: state for sg in ConvSubClasses for state in sg.all_states}
