from pyrogram import filters
import os
import re
from os import environ
from motor.motor_asyncio import AsyncIOMotorClient

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = 10786281
API_HASH = '5f42bc5562f6a1eb8bae8b77617186a0'
BOT_TOKEN ='2138045217:AAEcyEaMnPiVUftD3y3-FQb-mk1ktc4t1Dw'

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

# MongoDB information
client = AsyncIOMotorClient('mongodb+srv://swahilihit:swahilihit@cluster0.3nfk1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
DB2 = client['swahilihits']
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_file')

TG_BOT_WORKERS = int(os.environ.get("BOT_WORKERS", '4'))
thumb = os.environ.get('THUMBNAIL_URL', 'https://telegra.ph/file/516ca261de9ebe7f4ffe1.jpg')
OWNER_ID = 859704527
CUSTOM_START_MESSAGE = os.environ.get('START_MESSAGE','')
FILTER_COMMAND = os.environ.get('FILTER_COMMAND', 'add')
DELETE_COMMAND = os.environ.get('DELETE_COMMAND', 'del')
IS_PUBLIC = True if os.environ.get('IS_PUBLIC', 'True').lower() != 'false' else False
try:
    ADMINS=[859704527]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

def is_owner(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if user_id == OWNER_ID:
        return True
    else:
        return False

def is_admin(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if user_id in ADMINS:
        return True
    else:
        return False
def check_inline(_, __, update):
    try:
        user_id = update.from_user.id
    except:
        return False

    if IS_PUBLIC:
        return True
    elif user_id in ADMINS:
        return True
    else:
        return False

filters.admins = filters.create(is_admin)
filters.owner = filters.create(is_owner)
filters.inline = filters.create(check_inline)
