"""Singletons are created here: bot, database, dispatcher and so on."""
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from config import BOT_TOKEN
from database_api import MongoDB
from utils import inline_calendar

bot = Bot(BOT_TOKEN, parse_mode='Html')
storage = MongoStorage()
dp = Dispatcher(bot, storage=storage)
users_db = MongoDB()
calendar = inline_calendar.InlineCalendar()
