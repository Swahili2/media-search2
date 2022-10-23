from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
from info import filters
from plugins.database import db
    
@Client.on_message( filters.command('edit_admin') & filters.private)
async def group(client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        return
    await client.send_message(chat_id= message.from_user.id,text="chagua huduma unayotaka kufanya marekebisho",
            reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('Rekebisha Makundi', callback_data = 'kundi')],[InlineKeyboardButton('Rekebisha Aina', callback_data = 'aina')],[InlineKeyboardButton('Rekebisha startup sms', callback_data = 'startup')],[InlineKeyboardButton('Rekebisha mawasiliano', callback_data = 'namba')]])
        )
    
@Client.on_callback_query()
async def cbhandler(client: Client, query: CallbackQuery):
    if query.data == "kundi":
        await query.answer()
        mkv = await client.ask(text = " Samahani sana wateja wetu wa Kenya bado hatuja weka utaratibu mzuri.\n  hivi karibun tutaweka mfumo mzuri ili muweze kupata huduma zetu", chat_id = query.from_user.id)
    elif query.data == "aina":
        await query.answer()
    elif query.data == "startup":
        await query.answer()
    elif query.data == "namba":
        await query.answer()
