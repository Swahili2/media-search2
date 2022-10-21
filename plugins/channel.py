from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
from plugins.database import db
    
@Client.on_message( filters.command('edit_admin') & filters.private)
async def group(client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        return
    await client.send_message(chat_id= message.from_user.id,text="chagua huduma unayotaka kufanya marekebisho",
            reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('No', callback_data = 'delallclose')],[InlineKeyboardButton('No', callback_data = 'delallclose')],[InlineKeyboardButton('No', callback_data = 'delallclose')],[InlineKeyboardButton('No', callback_data = 'delallclose')]])
        )
    
