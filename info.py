import os

API_HASH = os.environ.get("API_HASH", "")
APP_ID = int(os.environ.get("APP_ID", ""))
DB_URI = os.environ.get("DATABASE_URL", "")
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_BOT_WORKERS = int(os.environ.get("BOT_WORKERS", '4'))
DB_NAME = os.environ.get("DATABASE_NAME", "InlineFilterBot")
thumb = os.environ.get('THUMBNAIL_URL', 'https://telegra.ph/file/516ca261de9ebe7f4ffe1.jpg')
OWNER_ID = int(os.environ.get('OWNER_ID'))
CUSTOM_START_MESSAGE = os.environ.get('START_MESSAGE','')
FILTER_COMMAND = os.environ.get('FILTER_COMMAND', 'add')
DELETE_COMMAND = os.environ.get('DELETE_COMMAND', 'del')
IS_PUBLIC = True if os.environ.get('IS_PUBLIC', 'True').lower() != 'false' else False
try:
    ADMINS=[OWNER_ID]
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
