import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from info import ADMINS
import os
from utils import save_file
logger = logging.getLogger(__name__)
lock = asyncio.Lock()


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files"""
    if lock.locked():
        await message.reply('Wait until previous process complete.')
    else:
        while True:
            last_msg = await bot.ask(text = "Forward me last message of a channel which I should save to my database.\n\nYou can forward posts from any public channel, but for private channels bot should be an admin in the channel.\n\nMake sure to forward with quotes (Not as a copy)", chat_id = message.from_user.id)
            try:
                last_msg_id = last_msg.forward_from_message_id
                if last_msg.forward_from_chat.username:
                    chat_id = last_msg.forward_from_chat.username
                else:
                    chat_id=last_msg.forward_from_chat.id
                await bot.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(f"This Is An Invalid Message, Either the channel is private and bot is not an admin in the forwarded chat, or you forwarded message as copy.\nError caused Due to <code>{e}</code>")
                continue

        msg = await message.reply('Processing...⏳')
        total_files = 0
        async with lock:
            try:
                total=last_msg_id + 1
                current=int(os.environ.get("SKIP", 2))
                nyav=0
                while True:
                    try:
                        message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        message = await bot.get_messages(
                            chat_id,
                            current,
                            replies=0
                            )
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                            else:
                                continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                    except Exception as e:
                        print(e)
                        pass
                    current+=1
                    nyav+=1
                    if nyav == 20:
                        await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                        nyav -= 20
                    if current == total:
                        break
                    else:
                        continue
            except Exception as e:
                logger.exception(e)
                await msg.edit(f'Error: {e}')
            else:
                await msg.edit(f'Total {total_files} Saved To DataBase!')

async def new_filter(client: Client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        return
    strid = str(uuid.uuid4())
    args = message.text.split(' ', 1)
    user_id = message.from_user.id
    if len(args) < 2:
        await message.reply_text("Use Correct format 😐", quote=True)
        return
    
    extracted = split_quotes(args[1])
    text = args[1].lower()
    msg_type = 'Text'
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = generate_button(extracted[1], strid)
        fileid = None
        if not reply_text:
            await message.reply_text("You cannot have buttons alone, give some text to go with it!", quote=True)
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
    mkv = await client.ask(text='naomba untumie maelezo kidogo mfano imetafsiriwa singo',chat_id = message.from_user.id)
    if not mkv.text:
        mkv.text=msg_type
    descp = mkv.text
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

    await save_file(text, reply_text, btn, fileid, alert, msg_type, strid,user_id,descp)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text = 'Share filter', switch_inline_query = text),
                InlineKeyboardButton(text = 'Try Here', switch_inline_query_current_chat = text)
            ]
        ]
    )
    await message.reply_text(f"<code>{text}</code> Added", quote = True, reply_markup = reply_markup)
