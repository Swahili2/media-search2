from pyrogram import Client
from info import filters
from plugins.status import handle_user_status
from utils import get_filter_results
@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    await handle_user_status(client,message)
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            await message.reply_text(f"<b>Bonyeza kitufe <b>(🔍Majibu ya Database : {len(files)})</b> Kisha subir kidogo,kisha chagua unachokipenda.\n\n💥Kwa urahisi zaidi kutafta chochote anza na aina kama ni  movie, series ,(audio ,video) kwa music , vichekesho kisha acha nafasi tuma jina la  kitu unachotaka mfano video jeje au audio jeje au movie extraction au series soz­</b>", reply_markup=get_reply_makup(search,len(files)))
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
