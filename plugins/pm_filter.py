from pyrogram import Client
import re
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from info import filters
from plugins.database import db
from plugins.status import handle_user_status,handle_admin_status
from utils import get_filter_results,is_user_exist,User
    
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
    gd=await db.get_db_status(int(user_id3))
    user_id4 = gd['ms_link']
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        searchi = message.text.lower()
        files = await get_filter_results(searchi,user_id3)
        if files:
            await message.reply_text(f"<b>Bonyeza kitufe <b>(🔍 Majibu ya Database : {len(files)})</b> Kisha chagua unachokipenda kwa kushusha chini\n\n💥Kwa urahisi zaidi kutafta chochote anza na aina kama ni  movie, series ,(audio ,video) kwa music , vichekesho kisha acha nafasi tuma jina la  kitu unachotaka mfano video jeje au audio jeje au movie extraction au series soz­</b>", reply_markup=get_reply_makup(searchi,len(files)))
        elif searchi.startswith('movie') or searchi.startswith('series') or searchi.startswith('dj'):
            await message.reply_text(text=f'Samahani **{searchi}** uliyotafta haipo kwenye database zetu.\n\nTafadhali bonyeza Button kisha ukurasa unaofuata ntumie jina la movie au series ntakupa jibu kwa haraka iwezekanavyo ili nii tafte',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='ADMIN',url=f'{user_id4}')]]))
            return
        else:
            return
        if not btn:
            return
@Client.on_message(filters.regex('@gmail.com') & filters.incoming)
async def groupprv(client, message): 
    text=message.text
    if " " not in text.strip() and "@gmail.com" in text.lower():
        group_status = await is_user_exist(message.from_user.id)
        user_id3='hrm45'
        if group_status:
            try:
                for user in group_status:
                    user_id3 = user.email
                    grp=user.group_id
                group_status = await is_user_exist(grp)
                for user in group_status:
                    grp=user.group_id
                if user_id3 == text.lower():
                    await message.reply_text('Hii email tayar Tulishaihifadhi kama unataka kuibadisha ntumie nyingene')
                else:
                    await message.reply_text('Tumeibadilisha kikamilifu')
                    await User.collection.update_one({'_id':message.from_user.id},{'$set':{'email':text.lower()}})
                    if await db.is_email_exist(message.from_user.id):
                        await message.reply_text(f'Tafadhali subir kidogo tutakupa taarifa tutakaipo iwezesha')
                        await client.send_message(chat_id=grp,text=f'Tafadhal iwezeshe email hii{message.text.strip()}.kisha ondoa uwezo kwenye email hii{user_id3}')
            except:
                await message.reply_text('Tumeihifadhi kikamilifu ukitaka kubadisha tuma tena email hiyo mpya')
                await User.collection.update_one({'_id':message.from_user.id},{'$set':{'email':text.lower()}})
                if await db.is_email_exist(message.from_user.id):
                    await message.reply_text(f'Tafadhal iwezeshe email hii{message.text.strip()}.kisha ondoa uwezo kwenye email hii{user_id3}')
        else:
            return
    else:
        await message.reply_text('Tafadhal ujumbe huu uliontumia sjauelewa Tafadhali kama n email:ntumie email tu bila neno jingine \nMfano  mohamed@gmail.com \n\nZingatia\n1.usiruke nafasi kwenye email yako  \n2.hakisha n gmail (hrmr5@gmail.com)\n3.hakikisha huongez neno lingine zaid ya email \n\nKwa salio lako tuma neno Salio \nZingatia lianze na herufi kubwa S na hizo nyingine ndogo\n\n Maelekezo mengine mchek hrm45')
        return
def get_reply_makup(query,totol):
    buttons = [
        [
            InlineKeyboardButton('🔍Majibu ya Database: '+ str(totol), switch_inline_query_current_chat=query),
        ]
        ]
    return InlineKeyboardMarkup(buttons)
