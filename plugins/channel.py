from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
@Client.on_message( filters.command('edit_admin') & filters.private)
async def group(client, message):
    
