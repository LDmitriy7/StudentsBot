"""Содержит все важные константы для бота (в том числе секретные)"""

from configparser import ConfigParser

parser = ConfigParser()
parser.read('../../config.ini')  # TODO: remove
parser.read('../config.ini')
parser.read('config.ini')

_bot = parser['Bot']
_conv_bot = parser['Conv Bot']
_application = parser['Application']
_channel = parser['Channel']
_telegraph = parser['Telegraph']
_banks = parser['Banks']
_admins = parser['Admins']

BOT_TOKEN = _bot['bot_token']
BOT_USERNAME = _bot['bot_username']
BOT_START_LINK = 'https://t.me/' + _bot["bot_username"] + '?start={}'
PAYMENTS_PROVIDER_TOKEN = _bot['payments_provider_token']

CONV_BOT_USERNAME = '@' + _conv_bot['bot_username']
GROUP_ADMIN_ID = _conv_bot.getint('group_admin_id')

API_ID = _application.getint('api_id')
API_HASH = _application['api_hash']

CHANNEL_USERNAME = '@' + _channel['main_channel']
CHANNEL_POST_URL = 't.me/' + _channel['main_channel'] + '/{}'

TELEGRAPH_TOKEN = _telegraph['access_token']

MONOBANK_PAYMENT_URL = _banks['monobank_payment_url']
PRIVAT_BANK_PAYMENT_url = _banks['privat_bank_payment_url']

MAIN_ADMIN_ID = _admins.getint('main_admin_id')
ADMIN_IDS = list(map(int, _admins['admin_ids'].split(',')))
