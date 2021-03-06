from aiogram.dispatcher.currents import CurrentObjects

from data_types import data_models, ProjectStatuses
from loader import users_db

__all__ = ['save_bid', 'save_profile', 'save_project', 'save_review']


@CurrentObjects.decorate
async def save_bid(*, user_id, text, sdata: dict) -> data_models.Bid:
    bid = data_models.Bid.from_dict({'worker_id': user_id, 'text': text, **sdata})
    bid.id = await users_db.add_bid(bid)
    return bid


@CurrentObjects.decorate
async def save_profile(*, user_id, sdata: dict, **kwargs) -> data_models.Profile:
    profile_data = dict(**sdata, **kwargs)
    profile = data_models.Profile.from_dict(profile_data)
    await users_db.update_account_profile(user_id, profile)
    return profile


@CurrentObjects.decorate
async def save_review(*, chat_id, text, user_name, sdata: dict) -> data_models.Review:
    chat = await users_db.get_chat_by_id(chat_id)
    project = await users_db.get_project_by_id(chat.project_id)

    rating = data_models.Rating.from_dict(sdata)
    review = data_models.Review(
        project.client_id,
        user_name,
        project.worker_id,
        project.id,
        project.data.subject,
        rating,
        text=text
    )
    review.id = await users_db.add_review(review)
    await users_db.update_project_status(project.id, ProjectStatuses.REVIEWED)
    return review


@CurrentObjects.decorate
async def save_project(status: str = ProjectStatuses.ACTIVE, *,
                       user_id, sdata: dict) -> data_models.Project:
    project_data = data_models.ProjectData.from_dict(sdata)
    project = data_models.Project(project_data, status, user_id, sdata.get('worker_id'))
    project.id = await users_db.add_project(project)
    return project
