from pyrogram import Client
import re
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
from plugins.status import handle_user_status,handle_admin_status
from utils import get_filter_results,is_user_exist
@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    
