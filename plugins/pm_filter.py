from pyrogram import Client
import re
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
from plugins.status import handle_user_status,handle_admin_status
from utils import get_filter_results,is_user_exist
    
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
        searchi = message.text.lower()
        files = await get_filter_results(searchi,user_id3)
        if files:
            await message.reply_text(f"<b>Bonyeza kitufe <b>(🔍 Majibu ya Database : {len(files)})</b> Kisha chagua unachokipenda kwa kushusha chini\n\n💥Kwa urahisi zaidi kutafta chochote anza na aina kama ni  movie, series ,(audio ,video) kwa music , vichekesho kisha acha nafasi tuma jina la  kitu unachotaka mfano video jeje au audio jeje au movie extraction au series soz­</b>", reply_markup=get_reply_makup(searchi,len(files)))
        elif searchi.startswith('movie') or searchi.startswith('series') or searchi.startswith('dj'):
            await message.reply_text(text=f'Samahani **{searchi}** uliyotafta haipo kwenye database zetu.\n\nTafadhali bonyeza Button kisha ukurasa unaofuata ntumie jina la movie au series ntakupa jibu kwa haraka iwezekanavyo ili nii tafte',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='ADMIN',user_id=int(user_id3))]]))
        else:
            return
        if not btn:
            return

def get_reply_makup(query,totol):
    buttons = [
        [
            InlineKeyboardButton('🔍Majibu ya Database: '+ str(totol), switch_inline_query_current_chat=query),
        ]
        ]
    return InlineKeyboardMarkup(buttons)
