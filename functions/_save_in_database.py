from data_types import data_classes, ProjectStatuses
from loader import users_db, dp
from aiogram.contrib.currents import SetCurrent
from aiogram import types

__all__ = ['save_bid', 'save_profile', 'save_project', 'save_review']


@SetCurrent.msg
@SetCurrent.udata
async def save_bid(*, msg: types.Message, udata: dict) -> data_classes.Bid:
    bid = data_classes.Bid.from_dict({'worker_id': msg.from_user.id, 'text': msg.text, **udata})
    bid.id = await users_db.add_bid(bid)
    return bid


@SetCurrent.user
async def save_profile(*, user: types.User, **kwargs) -> data_classes.Profile:
    udata = await dp.current_state().get_data()
    profile_data = dict(**udata, **kwargs)
    profile = data_classes.Profile.from_dict(profile_data)
    await users_db.update_account_profile(user.id, profile)
    return profile


@SetCurrent.msg
@SetCurrent.udata
async def save_review(*, msg: types.Message, udata: dict) -> data_classes.Review:
    chat = await users_db.get_chat_by_id(msg.chat.id)
    project = await users_db.get_project_by_id(chat.project_id)

    rating = data_classes.Rating.from_dict(udata)
    review = data_classes.Review(
        project.client_id,
        msg.from_user.full_name,
        project.worker_id,
        project.id,
        project.data.subject,
        rating,
        text=msg.text
    )
    review.id = await users_db.add_review(review)
    await users_db.update_project_status(project.id, ProjectStatuses.REVIEWED)
    return review


@SetCurrent.user
@SetCurrent.udata
async def save_project(status: str = ProjectStatuses.ACTIVE, *,
                       user: types.User, udata: dict) -> data_classes.Project:
    project_data = data_classes.ProjectData.from_dict(udata)
    project = data_classes.Project(project_data, status, user.id, udata.get('worker_id'))
    project.id = await users_db.add_project(project)
    return project
