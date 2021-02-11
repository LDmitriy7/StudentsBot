"""Содержит все важные константы для бота (в том числе секретные)"""

from configparser import ConfigParser

parser = ConfigParser()
parser.read('../../config.ini')  # TODO: remove
parser.read('../config.ini')  # TODO: remove
parser.read('config.ini')

_bot = parser['Bot']
_application = parser['Application']
_channel = parser['Channel']
_telegraph = parser['Telegraph']

BOT_TOKEN = _bot['bot_token']
START_LINK = 'https://t.me/' + _bot["bot_username"] + '?start={}'
LINKED_BOT = '@' + _bot['linked_conversation_bot']
PAYMENTS_PROVIDER_TOKEN = _bot['payments_provider_token']

API_ID = _application.getint('api_id')
API_HASH = _application['api_hash']

MAIN_CHANNEL = '@' + _channel['main_channel']
MAIN_POST_URL = 't.me/' + _channel['main_channel'] + '/{}'

TELEGRAPH_TOKEN = _telegraph['access_token']
