from aiogram import types

from data_types import data_classes, ProjectStatuses
from loader import users_db
from subfuncs.currents2 import Currents

__all__ = ['save_bid', 'save_profile', 'save_project', 'save_review']


@Currents.set
async def save_bid(*, msg: types.Message, sdata: dict) -> data_classes.Bid:
    bid = data_classes.Bid.from_dict({'worker_id': msg.from_user.id, 'text': msg.text, **sdata})
    bid.id = await users_db.add_bid(bid)
    return bid


@Currents.set
async def save_profile(*, user: types.User, sdata: dict, **kwargs) -> data_classes.Profile:
    profile_data = dict(**sdata, **kwargs)
    profile = data_classes.Profile.from_dict(profile_data)
    await users_db.update_account_profile(user.id, profile)
    return profile


@Currents.set
async def save_review(*, msg: types.Message, sdata: dict) -> data_classes.Review:
    chat = await users_db.get_chat_by_id(msg.chat.id)
    project = await users_db.get_project_by_id(chat.project_id)

    rating = data_classes.Rating.from_dict(sdata)
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


@Currents.set
async def save_project(status: str = ProjectStatuses.ACTIVE, *,
                       user: types.User, sdata: dict) -> data_classes.Project:
    project_data = data_classes.ProjectData.from_dict(sdata)
    project = data_classes.Project(project_data, status, user.id, sdata.get('worker_id'))
    project.id = await users_db.add_project(project)
    return project
