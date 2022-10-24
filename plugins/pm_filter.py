from pyrogram import Client
import re
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
from plugins.status import handle_user_status,handle_admin_status
from utils import get_filter_results,is_user_exist
from plugins.database import db
    
@Client.on_message( filters.command('edit_admin'))
async def group2(client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        return
    await client.send_message(chat_id= message.from_user.id,text="chagua huduma unayotaka kufanya marekebisho",
            reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('Rekebisha Makundi', callback_data = "kundii")],[InlineKeyboardButton('Rekebisha Aina', callback_data = "aina")],[InlineKeyboardButton('Rekebisha startup sms', callback_data = "startup")],[InlineKeyboardButton('Rekebisha mawasiliano', callback_data = "namba")]])
        )
    
@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    await handle_user_status(client,message)
    await handle_admin_status(client,message)
    group_status= await is_user_exist(message.chat.id)
    if group_status:
        for user in group_status:
            user_id3 = user.group_id
    else:
        return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        searchi = message.text
        files = await get_filter_results(searchi,user_id3)
        if files:
            await message.reply_text(f"<b>Bonyeza kitufe <b>(🔍Majibu ya Database : {len(files)})</b> Kisha subir kidogo,kisha chagua unachokipenda.\n\n💥Kwa urahisi zaidi kutafta chochote anza na aina kama ni  movie, series ,(audio ,video) kwa music , vichekesho kisha acha nafasi tuma jina la  kitu unachotaka mfano video jeje au audio jeje au movie extraction au series soz­</b>", reply_markup=get_reply_makup(searchi,len(files)))
        else:
            return
        if not btn:
            return
@Client.on_callback_query()
async def cbhandler2(client, query):
    if query.data == "kundii":
        mkv = await client.ask(text = " Samahani sana wateja wetu wa Kenya bado hatuja weka utaratibu mzuri.\n  hivi karibun tutaweka mfumo mzuri ili muweze kupata huduma zetu", chat_id = query.from_user.id)
        await query.answer('hellow')
    elif query.data == "aina":
        await query.answer()
    elif query.data == "startup":
        await query.answer()
    elif query.data == "namba":
        await query.answer()
def get_reply_makup(query,totol):
    buttons = [
        [
            InlineKeyboardButton('🔍Majibu ya Database: '+ str(totol), switch_inline_query_current_chat=query),
        ]
        ]
    return InlineKeyboardMarkup(buttons)
