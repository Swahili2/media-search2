from pyrogram import Client
import uuid
import io
from datetime import datetime,timedelta
import time
from plugins.database import db
from info import filters,CHANNELS
from utils import save_file,add_user,Media,User,is_user_exist,get_filter_results,get_file_details,is_group_exist,User
from pyrogram.types import CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from plugins.helper_funcs import (
    generate_button,
    upload_photo,
    split_quotes
)  
import os
import logging
logger = logging.getLogger(__name__)
BOT ={}
@Client.on_message(filters.command('total') & filters.owner)
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.private & filters.command('adddata'))
async def new_filtervip(client: Client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani hauruhusiw kutumia command hii Tafadhali  mchek @hrm45 akupe maelekezo")
        return
    strid = str(uuid.uuid4())
    args = message.text.split(' ', 1)
    user_id = message.from_user.id
    if len(args) < 2:
        await message.reply_text("Use Correct format 😐", quote=True)
        return
    nyva=BOT.get("username")
    if not nyva:
        botusername=await client.get_me()
        nyva=botusername.username
        BOT["username"]=nyva
    extracted = split_quotes(args[1])
    text = f'{args[1].lower()}.dd#.{user_id}'
    text = text.strip()
    ab = f'{args[1].lower()}'
    msg_type = 'Text'
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = generate_button(extracted[1], strid)
        fileid = None
        if not reply_text:
            await message.reply_text("huwez kutuma buttons peke yake , ongezea maneno kidogo", quote=True)
            return
        else:
            await message.reply_text("Tafadhali reply tangazo au posta ya movie yako kwa /adddata jina la movie au series\nMfano /adddata soz")
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        reply_text = ""
        btn = []
        fileid = None
        alert = None
        msg_type = 'Text'
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            replied = message.reply_to_message
            msg = replied.video
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            
            elif replied.photo:
                fileid = await upload_photo(replied)
                msg_type = 'Photo'
                if not fileid:
                    return
                reply_text = message.reply_to_message.caption.html
 
            else:
                await message.reply('Not Supported..!')
                return
            alert = None
        except:
            pass
            

    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = await upload_photo(message.reply_to_message)
            if not fileid:
                return
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Photo'

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Video'

    else:
        await message.reply('Not Supported..!')
        return
    usr = await db.get_db_status(message.from_user.id)
    x = 0
    p=[]
    usrr=' '
    ab7=' '
    for i in range(0,6):
        i+=1
        gs=f'g_{i}'
        if usr[gs] != 'hrm45':
            x+=1
            p.append(usr[gs].split('#@')[0])
            usrr=f'{usrr}\n{x}:{usr[gs].split("#@")[0]}'
    mkv1= await client.send_message(text=f'CHAGUA KIFURUSHI WAKILISHI YA KITU UNACHOTAKA KUHIFADHI \n (kwa kutuma namba ya kifurush husika kama itamilikiwa na zaid ya kifurushi kimoja tuna namba kifurushi kisha acha nafasi namba ya kifurushi kingine mfano 1 3 NOTE Media ina weza kumilikiwa na kifurushi 1 au viwili Tu sio zaidi)\n\n{usrr} \n\n Movie au video au picha za wakubwa haziruhusiwi kutumwa kwenye bot yetu ukijulikana utakuwa banned',chat_id = message.from_user.id)
    a,b = funask()
    id1=mkv1.id + 1
    while a==False:
        try:
            mkv = await client.get_messages("me",id1)
            if mkv.text!=None:
                a=True
            if (time.time()-b)>(60):
                await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 1 iliniweze kuhudumia na wengine")
                return
            if mkv.from_user.id != message.from_user.id :
                a=False
                id1=id1+1
        except:
            a=False
    try:
        ab5,ab6=mkv.text.split(" ",1)
        ab5= int(ab5)
        ab6 = int(ab6)
        if ab6>i<ab5 or ab5==ab6 or ab5==0 or ab6==0:
            await mkv.reply(text='tuma ujumbe sahihi kama ulivyo elekezwa idadi ya kutuma mwisho ni 6 anza upya')
            return
        ab7='y'
        ab2 = f'g_{ab5} g_{ab6}'
    except:
        pass
    if ab7!='y':
        try:
            ab00 = int(mkv.text)
            ab2 = f'g_{ab00} hrm44'
            if i<ab00 and ab00!=0:
                await mkv.reply(text='tuma ujumbe sahihi kama ulivyo elekezwa idadi ya kutuma mwisho ni 6 anza upya')
                return
        except:
            await mkv.reply(text='tuma ujumbe sahihi kama ulivyo elekezwa anza upya')
            return
    mkv1 = await client.send_message(text=f'tafadhal naomba utume bei(namba tu) ya {ab}kama ni bure tuma neno free mfano 500. (Kumbuka Hamna bei 0)',chat_id = message.from_user.id)
    a,b = funask()
    id1=mkv1.id+1
    while a==False:
        try:
            mkv = await client.get_messages("me",id1)
            if mkv.text!=None:
                a=True
            if (time.time()-b)>(60):
                await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 1 iliniweze kuhudumia na wengine")
                return
            if mkv.from_user.id != message.from_user.id :
                a=False
                id1=id1+1
        except:
            a=False
    try:
        ab1=int(mkv.text)
        if ab1==0:
            await mkv.reply(text='tuma ujumbe sahihi kama ulivyo elekezwa, tafadhali anza upya kwa usahihi')
            return
    except:
        await mkv.reply(text='tuma ujumbe sahihi kama ulivyo elekezwa ,tafadhali anza upya kwa usahihi')
        return
    mkv1= await client.send_message(text=f'naomba utume neno l kama utatuma {ab} kwa link au neno h kama n vipande vya {ab} ',chat_id = message.from_user.id)
    a,b = funask()
    id1=mkv1.id+1
    while a==False:
        try:
            mkv = await client.get_messages("me",id1)
            if mkv.text!=None:
                a=True
            if (time.time()-b)>(60):
                await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 1 iliniweze kuhudumia na wengine")
                return
            if mkv.from_user.id != message.from_user.id :
                a=False
                id1=id1+1
        except:
            a=False
    if mkv.text.lower()=='l' :
        mkv22 = await client.send_message(text=f'naomba untumie maelezo kidogo kwa hich ulichotuma mfano kama in movie unaeza andika "imetafsiriwa movie DJ murphy',chat_id = message.from_user.id)
        a,b = funask()
        id1=mkv22.id+1
        while a==False:
            try:
                mkv2 = await client.get_messages("me",id1)
                if mkv2.text!=None:
                    a=True
                if (time.time()-b)>(60):
                    await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 1 iliniweze kuhudumia na wengine")
                    return
                if mkv2.from_user.id != message.from_user.id :
                    a=False
                    id1=id1+1
            except:
                a=False
        mkv22 = await client.send_message(text=f'naomba utume link ya kupakua {ab} hii',chat_id = message.from_user.id)
        a,b = funask()
        id1 = mkv22.id+1
        while a==False:
            try:
                mkvl = await client.get_messages("me",id1)
                if mkvl.text!=None:
                    a=True
                if (time.time()-b)>(3*60):
                    await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 3 iliniweze kuhudumia na wengine")
                    return
                if mkvl.from_user.id != message.from_user.id :
                    a=False
                    id1=id1+1
            except:
                a=False
        if not mkvl.text:
            mkvl.text=msg_type
        descp = f'x.dd#.{mkv2.text}.dd#.{mkvl.text}.dd#.s'
    elif mkv.text.lower()=='h':
        mkv22 = await client.send_message(text='naomba untumie maelezo kidogo mfano imetafsiriwa singo',chat_id = message.from_user.id)
        a,b = funask()
        id1=mkv22.id+1
        while a==False:
            try:
                mkv1= await client.get_messages("me",id1)
                if mkv1.text!=None:
                    a=True
                if (time.time()-b)>(3*60):
                    await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 3 iliniweze kuhudumia na wengine")
                    return
                if mkv1.from_user.id != message.from_user.id :
                    a=False
                    id1=id1+1
            except:
                a=False
        if mkv1.text:
            dta='start'
            icount = 0
            while dta!='stop':
                stridm = str(uuid.uuid4())
                mkv22=await client.send_message(text = " Tuma video au document au audio au neno stop kama ushamaliza kutuma ili njumuishe kwenye tangazo hili", chat_id = message.from_user.id)
                a,b = funask()
                id1 = mkv22.id+1
                while a==False:
                    try:
                        mk= await client.get_messages("me",id1)
                        if mk.media!=None or mk.text!=None:
                            a=True
                        if (time.time()-b)>(10*60):
                            await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 10 iliniweze kuhudumia na wengine")
                            return
                        if mk.from_user.id != message.from_user.id :
                            a=False
                            id1=id1+1
                    except:
                        a=False
                if mk.media and not (mk.photo):
                    for file_type in ("document", "video", "audio"):
                        media = getattr(mk, file_type, None)
                        if media is not None:
                            media.file_type = file_type
                            media.caption = mk.caption
                            break
                    await client .send_cached_media(
                        chat_id = CHANNELS,
                        file_id = media.file_id,
                        caption = media.caption,
                        
                    )
                    media.caption = f'{media.caption}\n🌟 @Bandolako2bot 'if media.caption else '🌟 @Bandolako2bot'
                    media.file_name = f'p.dd#.h5'
                    await save_file(f'+{icount}.{strid}', media.caption, [], media.file_id, None, media.file_type, stridm,user_id,media.file_name,500,'normal')
                elif mk.text.lower()=='stop':
                    dta = 'stop'
                    await mk.reply(f'all file sent to database with id  {fileid}')
                    break
                else:
                    await mk.reply('tafadhali tuma ulichoambiwa')
                icount+=1
        descp = f'x.dd#.{mkv1.text}.dd#.data.dd#.m'
    try:
        if fileid:
            data1=await is_group_exist(message.from_user.id)
            if msg_type == 'Photo':
                await message.reply_photo(
                    photo = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
                await client.send_photo(
                    chat_id = CHANNELS,
                    photo = fileid,
                    caption = f'{reply_text}\n{message.from_user.mention}',
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
                
                for data2 in data1:
                    try:
                        await client.send_photo(
                            chat_id=int(data2.id),
                            photo = fileid,
                            caption = reply_text,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='📥 Download',url=f"https://t.me/{nyva}?start=subinps_-_-_-_{strid}")]])
                        )
                    except Exception as err:
                        await message.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")                    
            else:
                await message.reply_cached_media(
                    
                    file_id = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
                await client.send_cached_media(
                    chat_id = CHANNELS,
                    file_id = fileid,
                    caption = f'{reply_text}{message.from_user.mention}',
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
                for data2 in data1:
                    try:
                        await client.send_cached_media(
                            chat_id=int(data2.id),
                            file_id = fileid,
                            caption = reply_text,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='📥 Download',url=f"https://t.me/{nyva}?start=subinps_-_-_-_{strid}")]])
                        )
                    except:
                        pass
        else:
            await message.reply(
                text = reply_text,
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
            )
    except Exception as a:
        try:
            await message.reply(text = f"<b>❌ Error</b>\n\n{str(a)}\n\n<i>Join @CodeXBotzSupport for Support</i>")
        except:
            pass
        return

    await save_file(text, reply_text, [], fileid, alert, msg_type, strid,user_id,descp,ab1,ab2)
    text = text.split('.dd#.',1)[0]
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text = 'Share filter', switch_inline_query = text),
                InlineKeyboardButton(text = 'Try Here', switch_inline_query_current_chat = text)
            ]
        ]
    )
    await message.reply_text(f"<code>{text}</code> Added", quote = True, reply_markup = reply_markup)

@Client.on_message(filters.command('logger') & filters.owner)
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.private & filters.command('add'))
async def new_filter(client: Client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani hauruhusiw kutumia command hii tafadhali mchek @hrm45 akupe maelekezo")
        return
    strid = str(uuid.uuid4())
    args = message.text.split(' ', 1)
    user_id = message.from_user.id
    if len(args) < 2:
        await message.reply_text("Use Correct format 😐", quote=True)
        return
    
    extracted = split_quotes(args[1])
    text = f'{args[1].lower()}.dd#.{user_id}'
    text = text.strip()
    msg_type = 'Text'
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = generate_button(extracted[1], strid)
        fileid = None
        if not reply_text:
            await message.reply_text("huwez kutuma buttons peke yake , ongezea maneno kidogo", quote=True)
            return
        else:
            await message.reply_text("Tafadhali reply tangazo kwa /add jina la tangazo\n/add msaada")
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        reply_text = ""
        btn = []
        fileid = None
        alert = None
        msg_type = 'Text'
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            replied = message.reply_to_message
            msg = replied.document or replied.video or replied.audio or replied.animation or replied.sticker or replied.voice or replied.video_note or None
            if msg:
                fileid = msg.file_id
                if replied.document:
                    msg_type = 'Document'
                elif replied.video:
                    msg_type = 'Video'
                elif replied.audio:
                    msg_type = 'Audio'
                elif replied.animation:
                    msg_type = 'Animation'
                elif replied.sticker:
                    msg_type = 'Sticker'
                elif replied.voice:
                    msg_type = 'Voice'
                elif replied.video_note:
                    msg_type = 'Video Note'

                reply_text = message.reply_to_message.caption.html
            
            elif replied.photo:
                fileid = await upload_photo(replied)
                msg_type = 'Photo'
                if not fileid:
                    return
                reply_text = message.reply_to_message.caption.html
            
                    
            elif replied.text:
                reply_text = message.reply_to_message.text.html
                msg_type = 'Text'
                fileid = None
            else:
                await message.reply('Not Supported..!')
                return
            alert = None
        except:
            pass
            

    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid =await upload_photo(message.reply_to_message)
            if not fileid:
                return
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Photo'

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Video'

    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Audio'
   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Document'

    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Animation'

    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert =  generate_button(extracted[1], strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Sticker'

    elif message.reply_to_message and message.reply_to_message.voice:
        try:
            fileid = message.reply_to_message.voice.file_id
            reply_text, btn, alert = generate_button(message.reply_to_message.caption.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Voice'
    elif message.reply_to_message and message.reply_to_message.video_note:
        try:
            fileid = message.reply_to_message.video_note.file_id
            reply_text, btn, alert = generate_button(extracted[1], strid)
        except Exception as a:
            reply_text = ""
            btn = []
            alert = None
        msg_type = 'Video Note'
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = generate_button(message.reply_to_message.text.html, strid)
        except:
            reply_text = ""
            btn = []
            alert = None
    else:
        await message.reply('Not Supported..!')
        return
    mkv22 = await client.send_message(text='naomba untumie maelezo kidogo mfano imetafsiriwa singo',chat_id = message.from_user.id)
    a,b = funask()
    id1 = mkv22.id+1
    while a==False:
        try:
            mkvg = await client.get_messages("me",id1)
            if mkvg.text!=None:
                a=True
            if (time.time()-b)>(60):
                await client.send_message(chat_id = message.from_user.id,text=f" Tafadhali anza upya jitahidi kutuma ujumbe ndani ya dakika 1 iliniweze kuhudumia na wengine")
                return
            if mkvg.from_user.id != message.from_user.id :
                a=False
                id1=id1+1
        except:
            a=False
    if not mkvg.text:
        mkvg.text=msg_type
    descp = f'x.dd#.{mkvg.text}'
    try:
        if fileid:
            if msg_type == 'Photo':
                await message.reply_photo(
                    photo = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
            else:
                await message.reply_cached_media(
                    file_id = fileid,
                    caption = reply_text,
                    reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
                )
        else:
            await message.reply(
                text = reply_text,
                disable_web_page_preview = True,
                reply_markup = InlineKeyboardMarkup(btn) if len(btn) != 0 else None
            )
    except Exception as a:
        try:
            await message.reply(text = f"<b>❌ Error</b>\n\n{str(a)}\n\n<i>Join @CodeXBotzSupport for Support</i>")
        except:
            pass
        return

    await save_file(text, reply_text, btn, fileid, alert, msg_type, strid,user_id,descp,599,'normal')
    text = text.split('.dd#.',1)[0]
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text = 'Share filter', switch_inline_query = text),
                InlineKeyboardButton(text = 'Try Here', switch_inline_query_current_chat = text)
            ]
        ]
    )
    await message.reply_text(f"<code>{text}</code> Added", quote = True, reply_markup = reply_markup)

@Client.on_message(filters.private & filters.command('delete'))
async def del_filter(client: Client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani hauruhusiw kutumia command hii tafadhali mchek @hrm45 akupe maelekezo")
        return
    try:
        cmd, text1 = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>Mention the filtername which you wanna delete!</i>\n\n"
            f"<code>/delete filtername</code>\n\n"
            "Use /filters to view all available filters",
            quote=True
        )
        return
    text=f'{text1}.dd#.{message.from_user.id}'
    query = text.lower()
    filter={'text': query}
    details = await  get_filter_results('text1',message.from_user.id)
    filter['group_id'] = message.from_user.id
    found =await Media.count_documents(filter)
    if int(found) >=1:
        for dt in details:
            for ad in await get_file_details(dt.id):
               await Media.collection.delete_one({'text':ad.text})
        await Media.collection.delete_one(filter)
        await message.reply_text(
            f"<code>{text.split('.dd#.')[0]}</code>  deleted successful.",
            quote=True
        )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)
@Client.on_message(filters.private & filters.command('filters'))
async def get_all(client: Client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani hauruhusiw kutumia command hii tafadhali mchek @hrm45 akupe maelekezo")
        return
    text = ''
    texts = await get_filter_results(text,message.from_user.id)
    count = await Media.count_documents({'group_id':message.from_user.id})
    if count:
        filterlist = f"<b>Bot have total {count} filters</b>\n\n"

        for text in texts:
            keywords = f" ○  <code>{text.text.split('.dd#')[0]}</code>\n"
            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("<code>", "").replace("</code>","").replace('<b>', '').replace('</b>', ''))) as keyword_file:
                sts = await message.reply('<i>Please wait..</i>')
                keyword_file.name = "filters.txt"
                await message.reply_document(
                    document=keyword_file
                )
                await sts.delete()
            return
    else:
        filterlist = f"<b>Bot have no filters.!</b>"

    await message.reply_text(
        text=filterlist,
        quote=True
    )
    
@Client.on_message(filters.command('delall') & filters.owner)
async def delallconfirm(Client, message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Yes', callback_data = 'delall'),
                InlineKeyboardButton('No', callback_data = 'delallclose')
            ]
        ]
    )
    await message.reply_text(
        f"This will delete all of your filters.\nAre you sure you want do this.?",
        reply_markup = reply_markup,
        quote=True
    )
@Client.on_message((filters.private | filters.group) & filters.command('niunge'))
async def addconnection(client,message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani hauruhusiw kutumia command hii tafadhali mchek @hrm45 akupe maelekezo")
        return
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Samahan wewe ni anonymous(bila kujulikana) admin tafadhali nenda kweny group lako edit **admin permission** remain anonymouse kisha disable jaribu tena kutuma /niunge.Kisha ka enable tena")
    chat_type =f"{ message.chat.type}"
    
    if chat_type == "ChatType.PRIVATE":
        await message.reply_text(
                "Samahan add hii bot kama admin kwenye group lako kisha tuma command hii <b>/niunge </b>kwenye group lako",
                quote=True
            )
        return

    elif chat_type in ["ChatType.GROUP","ChatType.SUPERGROUP"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        st.status=(f"{st.status}".split(".")[1])
        if not(
            st.status == "ADMINISTRATOR"
            or st.status == "OWNER"
        ):
            await message.reply_text("lazima uwe  admin kwenye group hili!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, Make sure I'm present in your group!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        st.status=(f"{st.status}".split(".")[1])
        if st.status == "ADMINISTRATOR":
            group_details= await is_user_exist(group_id)
            for file in group_details:
                user_id2=file.group_id
            
            if not group_details :
                if await is_group_exist(message.from_user.id):
                    await message.reply_text("Samahani tunaruhusu kikundi kimoja tu kumunga muhsin kuepuka usumbufu kwa wateja tuma /ondoa kikund cha mwanzo kisha tuma /niunge  kwenye kikundi hiki **\nkumbuka kuondoa group tunaondoa hadi waliojiunga kwenye database yetu kupitia kikundi hiko** ")
                    return
                await add_user(group_id,userid,'group')
                await message.reply_text(
                    f"Tumeliunganisha kikamilifu Sasa unaweza kuendelea kuongezea muv/series posters audio video n.k ukiwa private kwa kureply ujumbe wako kisha /add kisha jina LA text,movie,series n.k kama ndio unaanza uadmin tafadhali tuna neno /edit_admin ukiwa private kisha fuata maelekezo!",
                    quote=True,
                )
                if chat_type in ["group", "supergroup","private"]:
                    await client.send_message(
                        userid,
                        f"Asante kwa kutuamini umefanikiwa kuunganisha group lako tuma /help kupata muongozo!",
                        parse_mode="md"
                    )
                    return
           
            elif userid !=user_id2:
                ttli = await client.get_users(user_id2)
                await message.reply_text(
                    f"Samahan hili group tayar limeshaunganishwa na admin **{ttli.first_name}** Msimaiz wangu kanikataza ku add wasimaz wawili kwenye group moja kama mnahitaj mabadiliko mcheki @hrm45!",
                    quote=True
                )
            else:
                ttli = await client.get_users(user_id2)
                await message.reply_text(
                    f"Samahani admin **{ttli.first_name}** hili group tayar umeshaliunga kulitoa  tuma command /ondoa !",
                    quote=True
                )
        else:
            await message.reply_text("Ni add admin kwenye group lako kisha jaribu tena", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('Kuna tatizo tafadhali jaribu badae!!!.', quote=True)
        return

@Client.on_message((filters.private | filters.group | filters.channel) & filters.command("ondoa"))
async def removegroup(client,message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        await message.reply_text("Samahani huruhusiwi kutumia command  hii tafadhali mchek @hrm45 akupe maelekezo")
        return
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Samahan wewe ni anonymous(bila kujulikana) admin tafadhali nenda kweny group lako edit **admin permission** remain anonymouse kisha disable jaribu tena kutuma /niunge.Kisha ka enable tena")
    chat_type =f"{ message.chat.type}"
    
    if chat_type == "ChatType.PRIVATE":
        await message.reply_text(
                "Samahan add hii bot kama admin kwenye group lako kisha tuma command hii <b>/niunge </b>kwenye group lako",
                quote=True
            )
        return

    elif chat_type in ["ChatType.GROUP","ChatType.SUPERGROUP"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        st.status=(f"{st.status}".split(".")[1])
        if not(
            st.status == "ADMINISTRATOR"
            or st.status == "OWNER"
        ):
            await message.reply_text("lazima uwe  admin kwenye group hili!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, Make sure I'm present in your group!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        st.status=(f"{st.status}".split(".")[1])
        if st.status == "ADMINISTRATOR":
            
            group_details= await is_user_exist(group_id)
            for file in group_details:
                user_id2=file.group_id
            if group_details and userid==user_id2:
                await User.collection.delete_one({'_id':group_id})
                await User.collection.deleteMany({'group_id':group_id})
                await message.reply_text(
                    f"tumeliondoa kikamilifu kuliunga tena tuma command /niunge",
                    quote=True
                )
            elif not (group_details):
                ttli = await client.get_users(user_id2)
                await message.reply_text(
                    f"Samahani admin **{ttli.first_name}** hili group halipo  kwenye database zetu tuma /niunge kuliunga!",
                    quote=True
                )
            elif userid !=user_id2:
                ttli = await client.get_users(user_id2)
                await message.reply_text(
                    f"Samahani hili group limeungwa na admin   admin **{ttli.first_name}** hili group yeye mwenyewe ndio unaweza kulitoa!",
                    quote=True
                )
        else:
            await message.reply_text("Ni add admin kwenye group lako kisha jaribu tena", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('Kuna tatizo tafadhali jaribu badae!!!.', quote=True)
        return
@Client.on_message(filters.private & filters.command("add_admin") & filters.owner)
async def ban(c,m):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to add access to any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/add_admin admin_id duration_in days link`\n\n"
            f"Eg: `/add_admin 1234567 28 Umepata ofa ya Siku 3 zaidi.`\n"
            f"This will add user with id `1234567` for `28` days for the reason `ofa siku 3 zaidi`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        link = m.command[3]
        ban_reason = 'Kwa ajili ya kumtumia swahili robot kuuzia movie na series '
        ban_log_text = f"Adding user {user_id} for {ban_duration} days for the reason {ban_reason} ."
        try:
            await c.send_message(
                user_id,
                f"Asante kwa uaminifu wako kwetu \n\n **🧰🧰 KIFURUSHI CHAKO 🧰🧰** \n\n🗓🗓**siku___ siku  {ban_duration}(+ofa)**\n\n🎁🎁Kwa ajili ya ** __  {ban_reason}__**\n\n Umeungwa kikamilifu"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            
            ban_log_text += f"\n\nNmeshindwa kumtaarifu tafadhali jaribu tena! \n\n`{traceback.format_exc()}`"
        adminexist=await db.is_admin_exist(user_id)
        if not adminexist :
            strid = str(uuid.uuid4())
            await db.add_admin(user_id)
            await db.add_acc(strid,user_id,"all",user_id,9999)
        await db.ban_user(user_id, ban_duration, ban_reason,link)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n",
            quote=True
        )
@Client.on_message(filters.private & filters.command('salio'))
async def get_statuss(bot,message):
    status= await db.is_admin_exist(message.from_user.id)
    if status:
        async for user in await db.get_user(message.from_user.id):
            salio =user['ban_status']
            salio = datetime.fromisoformat(salio['banned_on'])+timedelta(days=salio['ban_duration'])
        filters = await get_filter_results('',message.from_user.id)
        filters_no = 0
        text = 0
        photo = 0
        video = 0
        audio = 0
        document = 0
        animation = 0
        sticker = 0
        voice = 0 
        videonote = 0 
        for filter in filters:
            type = filter['type']
            if type == 'Text':
                text += 1 
            elif type == 'Photo':
                photo += 1 
            elif type == 'Video':
                video += 1 
            elif type == 'Audio':
                audio += 1 
            elif type == 'Document':
                document += 1
            elif type == 'Animation':
                animation += 1
            elif type == 'Sticker':
                sticker += 1 
            elif type == 'Voice':
                voice += 1
            elif type == 'Video Note':
                videonote += 1 

            filters_no += 1
    
        user_collection = await User.count_documents({'group_id': message.from_user.id})
    
        stats_text = f"""<b>Statistics</b>
    
Total groups: {user_collection}
Total filters: {filters_no}
Text filters: {text}
Photo filters: {photo}
Video filters: {video}
Audio filters: {audio}
Document filters: {document}
Animation filters: {animation}
Sticker filters: {sticker}
Voice filters: {voice}
Video Note filters: {videonote}

Salio lako:Litaisha tarehe {salio} ::Kumbuka kufanya malipo mapema wateja wako wafurahie huduma za Swahili robot """
        await message.reply_text(stats_text)
    users=await db.get_acc(message.from_user.id)
    salio='Vifurushi Vyako ulivyojiunga kupata huduma za movies,series, tamthilia n.k : \n\n'
    a=1
    async for user in users:
        a=2
        if user['file_id'].startswith('g_'):
            sd= await db.get_db_status(user['db_name'])
            g2 = user['file_id']
            sd = sd[g2].split('#@')[0]
            salio+=f"{sd}:Kitaisha tarehe :{datetime.fromisoformat(user['ban_status']['banned_on'])+timedelta(days=user['ban_status']['ban_duration'])}\n\n"
        else:
            sd = await get_file_details(user['file_id'])
            for sd1 in sd:
                salio+=f"{sd1.text.split('.dd#.')[0]}:Kitaisha tarehe :{datetime.fromisoformat(user['ban_status']['banned_on'])+timedelta(days=user['ban_status']['ban_duration'])}\n\n"
    if a==1:
        await message.reply_text('Vifurushi Vyako ulivyojiunga kupata huduma za movies,series, tamthilia n.k : \n\nHamna kifurushi ulichojiunga nacho,Tafadhali kuwa huru kununua kifurushi vyetu kwa bei rahisi')
    else:
        await message.reply_text(salio)

@Client.on_callback_query(filters.regex("^delall$") & filters.owner)
async def delall(client: Client, query):
    await del_all(query.message)

@Client.on_callback_query(filters.regex("^delallclose$") & filters.owner)
async def delcancel(client: Client, query):
    await query.edit_message_text(
        text = 'Process Cancelled',
        reply_markup = None
    )
    return
def funask():
    a=False
    b=time.time()
    return a,b
