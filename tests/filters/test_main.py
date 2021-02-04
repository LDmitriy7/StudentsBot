from filters import DeepLinkPrefix, QueryPrefix
from keyboards.inline_funcs import Prefixes
from aiogram import types
from loader import users_db
import asyncio


async def get_all_projects():
    accounts = await users_db.get_all_projects()
    pids = [str(i['_id']) for i in accounts]
    return pids


msg = types.Message()
query = types.CallbackQuery()
command_start = '/start {prefix}{payload}'
project_ids = asyncio.run(get_all_projects())
NORMAL_PREFIXES = Prefixes.all()


def test_normal_prefixes():
    for payload in project_ids:
        for prefix in NORMAL_PREFIXES:
            msg.text = command_start.format(prefix=prefix, payload=payload)
            _filter = DeepLinkPrefix(prefix)
            assert _filter(msg) == {'payload': payload}


def test_normal_prefixes2():
    for payload in project_ids:
        for prefix in NORMAL_PREFIXES:
            query.data = prefix + payload
            _filter = QueryPrefix(prefix)
            assert _filter(query) == {'payload': payload}


def test_broken_prefixes():
    for payload in project_ids:
        for prefix in NORMAL_PREFIXES:
            msg.text = command_start.format(prefix=prefix[:-1], payload=payload)
            _filter = DeepLinkPrefix(prefix)
            assert _filter(msg) is False


def test_broken_prefixes2():
    for payload in project_ids:
        for prefix in NORMAL_PREFIXES:
            query.data = prefix[:-1] + payload
            _filter = QueryPrefix(prefix)
            assert _filter(query) is False