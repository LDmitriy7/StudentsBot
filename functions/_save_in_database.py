from data_types import data_classes, ProjectStatuses
from loader import users_db, dp
from subfuncs import decorators as current
from aiogram import types

__all__ = ['save_bid', 'save_profile', 'save_project']


async def save_bid(client_id: int, project_id: str, worker_id: int, text: str) -> str:
    bid = data_classes.Bid.from_dict(locals())
    bid_id = await users_db.add_bid(bid)  # сохранение заявки
    return bid_id


@current.set_user
async def save_profile(user: types.User = None, **kwargs) -> data_classes.Profile:
    udata = await dp.current_state().get_data()
    profile_data = dict(**udata, **kwargs)
    profile = data_classes.Profile.from_dict(profile_data)
    await users_db.update_account_profile(user.id, profile)
    return profile


@current.set_user
@current.set_udata
async def save_project(status: str = ProjectStatuses.ACTIVE,
                       user: types.User = None, udata: dict = None) -> data_classes.Project:
    project_data = data_classes.ProjectData.from_dict(udata)
    project = data_classes.Project(project_data, status, user.id, udata.get('worker_id'))
    project.id = await users_db.add_project(project)
    return project
