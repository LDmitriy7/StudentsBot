from questions.misc import ConvStatesGroup
from questions import *

__all__ = ['create_post', 'personal_project']

ALL_CONV_STATES = {}  # state_name: state

for state_group in ConvStatesGroup.__subclasses__():
    states = {state.state: state for state in state_group.all_states}
    ALL_CONV_STATES.update(states)

if __name__ == '__main__':
    for k, v in ALL_CONV_STATES.items():
        print(k, v, v.group, v.question, sep='\n\t', end='\n\n')
