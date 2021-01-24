import os
import subprocess

server_py = ['server.py', """\
\"""Main script, starts bot in long-polling mode.\"""
from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    import logging

    import middlewares
    import handlers

    logging.basicConfig(level=30)

    dp.throttling_rate_limit = 3
    dp.no_throttle_error = True


if __name__ == '__main__':
    from aiogram import executor
    from loader import dp

    executor.start_polling(dp, on_startup=on_startup)

__all__ = ['handlers', 'middlewares']

"""]

loader_py = ['loader.py', """\
\"""Singletons are created here: bot, database, dispatcher and so on.\"""
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from config import BOT_TOKEN
from database_api import MongoDB

bot = Bot(BOT_TOKEN, parse_mode='Html')
storage = MongoStorage()
dp = Dispatcher(bot, storage=storage)
db = MongoDB()
"""]

database_api = ['database_api.py', """\
\"""Содержит класс для работы с базой данных\"""


class MongoDB:
    pass
"""]

config_py = ['config.py', """\
\"""Содержит все важные константы для бота (в том числе секретные)\"""
import os

BOT_TOKEN = os.getenv('BOT_TOKEN1')
"""]

_gitignore = ['.gitignore', """\
# My files
config.py

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# IntelliJ project files
.idea
*.iml
out
gen
"""]

mw_init_py = ['__init__.py', """\
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from middlewares.main import *

dp.setup_middleware(LoggingMiddleware())
"""]

mw_main_py = ['main.py', """\
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
"""]

states_main_py = ['main.py', """\
from aiogram.dispatcher.filters.state import State, StatesGroup
"""]

states_init_py = ['__init__.py', """\
from states.main import *
"""]

kb_markup_py = ['markup.py', """\
from aiogram.types import ReplyKeyboardMarkup
"""]

kb_inline_py = ['inline.py', """\
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
"""]

handlers_init_py = ['__init__.py', """\
from handlers import *
"""]


# ---------- end describing ----------


def create_files(packages: dict):
    for folder, files in packages.items():

        if folder != '.':
            os.mkdir(folder)
            files.insert(0, '__init__.py')  # will be appended if __init__.py in files

        for file in files:
            if isinstance(file, str):
                filename, file_text = file, ''
            else:
                filename, file_text = file

            with open(f'{folder}/{filename}', 'a') as fp:
                fp.write(file_text)


PACKAGES = {
    '.': [server_py, loader_py, config_py, _gitignore, database_api],
    'keyboards': [kb_markup_py, kb_inline_py],
    'texts': ['main.py'],
    'states': [states_init_py, states_main_py],
    'handlers': [handlers_init_py],
    'questions': [],
    'middlewares': [mw_init_py, mw_main_py],
    'utils': [],
}
SITE_PACKAGES = ['aiogram', 'motor', 'pymongo']

create_files(PACKAGES)

# make virtual env, install packages, make requirements.txt
os.system('python3 -m venv venv')

site_packages_list = [f'pip3 install {p};' for p in SITE_PACKAGES]
site_packages_text = '\n'.join(site_packages_list)

subscript_name = 'installer.sh'
subscript_text = f"""\
source venv/bin/activate;
{site_packages_text}
pip3 freeze > requirements.txt
"""

with open(subscript_name, 'w') as fp:
    fp.write(subscript_text)

os.system('python3 -m venv venv')
os.system(f'/bin/bash {subscript_name}')
os.remove(subscript_name)

# make git-repository
os.system('git init')
os.system('git add .')
os.system('git commit -m "first commit"')
