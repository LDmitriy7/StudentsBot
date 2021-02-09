from database_api import MongoDB
import type_classes as datatypes
from pytest import mark
import asyncio

_db = MongoDB()
pdata = {"work_type": "Дипломная", "subject": "Unix", "date": "2021-02-17",
         "description": "Dobrý Tak to bude asi nejlepší lepší", "price": None, "note": None,
         "files": [
             ["photo",
              "AgACAgIAAxkBAAJKgGAgRIGN6b7yIw4Ue_s2WeJrMVEqAAJDtTEb1iLoSOjsCHIDUg8emucymy4AAwEAAwIAA3kAA21RAgABHgQ"]]
         }
pdata = datatypes.ProjectData(**pdata)
project = {
    "client_id": 724477101, "worker_id": None, "status": "Активен",
    "post_url": "t.me/help_students7/83"
}
project = datatypes.Project(**project, data=pdata)

bid = datatypes.Bid(**{
    "client_id": 1478623483, "worker_id": 724477101,
    "project_id": "6016f6084ca817b3e3f8fa79", "text": "Здравствуйте, помогу прям сейчас"
})

chat = datatypes.Chat(**{
    "project_id": "6016f6084ca817b3e3f8fa79", "chat_type": "client", "user_id": 1478623483,
    "link": "https://t.me/joinchat/IERuxYC7bh_h4wTL", "pair_id": -545651958
})

rating = datatypes.Rating(**{
    "quality": 4, "contact": 5, "terms": 4
})

review = datatypes.Review(**{
    "client_id": 1478623483, "worker_id": 724477101,
    "project_id": "601975fd7a44a2358740a40e", "rating": rating, "text": "Спасибо!", "client_name": "Максим Некрасов"
})


@mark.asyncio
async def test_add_project():
    coro = _db.add_project(project)
    result = await coro
    print(result)


@mark.asyncio
async def test_add_bid():
    coro = _db.add_bid(bid)
    result = await coro
    print(result)


@mark.asyncio
async def test_add_chat():
    coro = _db.add_chat(-541355719, chat)
    result = await coro
    print(result)


@mark.asyncio
async def test_add_review():
    coro = _db.add_review(review)
    result = await coro
    print(result)


@mark.asyncio
async def test_get_all_accounts():
    coro = _db.get_all_accounts()
    result = await coro
    print(result)


# asyncio.run(test_add_project())
# asyncio.run(test_add_bid())
# asyncio.run(test_add_chat())
# asyncio.run(test_add_review())
asyncio.run(test_get_all_accounts())
