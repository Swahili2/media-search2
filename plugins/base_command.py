from info import filters
from utils import get_file_details,get_filter_results
from pyrogram  import Client
from plugins.database import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from plugins.strings import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, MARKDOWN_HELP

start_keyboard = [
    [
        InlineKeyboardButton(text = '🤔 Help', callback_data = "help"),
        InlineKeyboardButton(text = '🤖 About', callback_data = "about")
    ],
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close"),
        InlineKeyboardButton(text = 'Search Here', switch_inline_query_current_chat = '')
    ]
]

start_keyboard_c = [
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = "about"),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = "close")
    ],
    [
        InlineKeyboardButton(text = 'Search Here', switch_inline_query_current_chat = '')
    ]
]

help_keyboard = [
    [
        InlineKeyboardButton(text = '✏️ Markdown Helper ✏️', callback_data = 'markdownhelper')
    ],
    [
        InlineKeyboardButton(text = '🤖 About', callback_data = 'about'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard = [
     [
        InlineKeyboardButton(text = '🤔 Help', callback_data = 'help'),
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

about_keyboard_c = [
    [
        InlineKeyboardButton(text = 'Close 🔒', callback_data = 'close')
    ]
]

markdown_keyboard = [
    [
        InlineKeyboardButton(text = '🔙 Back', callback_data = 'help')
    ]
]

@Client.on_message(filters.command('start') & filters.private)
async def start_msg_admins(client, message):
    if await db.is_admin_exist(message.from_user.id):
        reply_markup = InlineKeyboardMarkup(start_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(start_keyboard_c)
    text = START_MESSAGE.format(
        mention = message.from_user.mention,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name,
        user_id = message.from_user.id,
        username = '' if message.from_user.username == None else '@'+message.from_user.username
    )
    usr_cmdall1 = message.text
    cmd=message
    if usr_cmdall1.startswith("/start subinps"):
        ban_status = await db.get_ban_status(cmd.from_user.id)  
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                f_caption=files.reply
            strg=files.descp.split('.dd#.')[3]
            if filedetails:
                if filedetails:
                    if strg.lower() == 'm':
                        filez=await get_filter_results(file_id)
                        for file in reversed(filez):
                            filedetails = await get_file_details(file.file_id)
                            for files in filedetails:
                                f_caption=files.reply
                                await bot.send_cached_media(
                                    chat_id=cmd.from_user.id,
                                    file_id=files.file,
                                    caption=f_caption
                                )
                        return
                    elif strg.lower() == 's':
                        link = files.descp.split('.dd#.')[2]
                        f_caption =f'\n🌟 @Bandolako2bot \n\n **💥Series  zetu zote zipo google drive, Kama huwezi kufungua link zetu tafadhali bonyeza 📪 ADD EMAIL kisha fuata maelekezo**'
                        await bot.send_photo(
                            chat_id=cmd.from_user.id,
                            photo=files.file,
                            caption=f_caption,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📪 ADD EMAIL",callback_data = "addemail")],[InlineKeyboardButton("🔗 GOOGLE LINK",url= link)]])
                        )
                        return
                     
                else:
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text=f"Samahani **{cmd.from_user.first_name}** nmeshindwa kukuruhusu kendelea kwa sababu muv au sizon uliochagua ni za kulipia\n Tafadhal chagua nchi uliopo kuweza kulipia kifurushi",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🇹🇿 TANZANIA", callback_data = "tanzania"),
                                    InlineKeyboardButton("🇰🇪 KENYA",callback_data ="kenya" )
                                ]
                            ]
                        )
                    )
                    return
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    else:
        await message.reply(
            text = text,
            quote = True,
            reply_markup = reply_markup,
            disable_web_page_preview = True
        )
    
@Client.on_message(filters.command('help') & filters.private)
async def help_msg(client, message):
    await message.reply(
        text = HELP_MESSAGE,
        quote = True,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )

@Client.on_message(filters.command('about') & filters.private)
async def about_msg(client, message):
    user_id = message.from_user.id
    if await db.is_admin_exist(user_id):
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await message.reply(
        text = ABOUT_MESSAGE,
        quote = True,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )

@Client.on_callback_query(filters.regex(r'^close$'))
async def close_cbb(client, query):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass

@Client.on_callback_query(filters.regex(r'^help$'))
async def help_cbq(client, query):
    await query.edit_message_text(
        text = HELP_MESSAGE,
        reply_markup = InlineKeyboardMarkup(help_keyboard)
    )
    
@Client.on_callback_query(filters.regex('^about$'))
async def about_cbq(client, query):
    user_id = query.from_user.id
    if await db.is_admin_exist(user_id):
        reply_markup = InlineKeyboardMarkup(about_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(about_keyboard_c)
    await query.edit_message_text(
        text = ABOUT_MESSAGE,
        reply_markup = reply_markup,
        disable_web_page_preview = True
    )
    
@Client.on_callback_query(filters.regex('^markdownhelper$'))
async def md_helper(client, query):
    await query.edit_message_text(
        text = MARKDOWN_HELP,
        reply_markup = InlineKeyboardMarkup(markdown_keyboard),
        disable_web_page_preview = True,
        parse_mode = 'html'
    )
