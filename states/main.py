"""Содержит все наборы состояний бота"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class ConvStatesGroup(StatesGroup):
    questions: dict = {}

    @classmethod
    def attach_questions(cls, questions: dict):
        """Questions: {state_name: Quest}"""
        group_name = cls.__name__

        for state_name, question in questions.items():
            q = {f'{group_name}:{state_name}': question}
            cls.questions.update(q)


class CreatePost(ConvStatesGroup):
    work_type = State()
    subject = State()
    date = State()
    description = State()
    price = State()
    note = State()
    file = State()
    confirm = State()


class PersonalProject(ConvStatesGroup):
    work_type = State()
    subject = State()
    date = State()
    description = State()
    price = State()
    note = State()
    file = State()
    worker = State()
    confirm = State()


class Registration(ConvStatesGroup):
    nickname = State()
    phone = State()
    email = State()
    subjects = State()
    about_self = State()
    works = State()


class MiscStates(StatesGroup):
    change_subject = State()
    bid_text = State()


ALL_STATES_GROUPS = {s: s.all_states_names for s in ConvStatesGroup.__subclasses__()}

if __name__ == '__main__':
    CreatePost.attach_questions({'work_type': 'test123', 'price': 45})
    print(CreatePost.questions)
