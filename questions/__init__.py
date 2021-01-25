from questions.misc import ConvStatesGroup
from questions import *

__all__ = ['create_post']

ALL_CONV_STATES = {}  # state_name: state

for state_group in ConvStatesGroup.__subclasses__():
    states = {state.state: state for state in state_group.all_states}
    ALL_CONV_STATES.update(states)

print(ALL_CONV_STATES)
