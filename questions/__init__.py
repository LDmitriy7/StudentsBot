"""Contain all questions (ConvStatesGroups with question for each state)."""

from questions import create_post, personal_project
from questions.misc import ConvStatesGroup

ConvSubClasses = ConvStatesGroup.__subclasses__()

ALL_CONV_STATES_GROUPS = {sg: sg.all_states_names for sg in ConvSubClasses}
ALL_CONV_STATES = {state.state: state for sg in ConvSubClasses for state in sg.all_states}

# if __name__ == '__main__':
#     from pprint import pp
#
#     for sg, state_names in ALL_CONV_STATES_GROUPS.items():
#         print(sg)
#         for state in sg.all_states:
#             print(f'\t{state}', f'{state.question}\n', sep='\n\t\t')
#     print()
#     pp(ALL_CONV_STATES_NAMES)
