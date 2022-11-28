from info import filters
from utils import get_file_details,get_filter_results
from pyrogram  import Client
from plugins.database import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,ForceReply
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

@Client.on_message( filters.command('edit_admin') & filters.private )
async def group2(client, message):
    status= await db.is_admin_exist(message.from_user.id)
    if not status:
        return
    await client.send_message(chat_id= message.from_user.id,text="chagua huduma unayotaka kufanya marekebisho",
            reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('Rekebisha Makundi', callback_data = "kundii")],[InlineKeyboardButton('Rekebisha Aina', callback_data = "aina")],[InlineKeyboardButton('Rekebisha Startup sms', callback_data = "startup")],[InlineKeyboardButton('Rekebisha Mawasiliano', callback_data = "namba")]])
        )
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
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                f_caption=files.reply
                group_id = files.group_id
            ban_status = await db.get_ban_status(group_id) 
            
            if await db.is_acc_all_exist(cmd.from_user.id,group_id):
                akg = await client.send_message(chat_id=cmd.from_user.id,text="Please wait")
            elif not await db.is_acc_exist(cmd.from_user.id,file_id):
                await client.send_message(
                        chat_id=cmd.from_user.id,
                        text=f"Samahani **{cmd.from_user.first_name}** nmeshindwa kukuruhusu kendelea kwa sababu muv au sizon uliochagua ni za kulipia\n Tafadhal chagua nchi uliopo kuweza kulipia uweze kuitazama",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("🇹🇿 TANZANIA", callback_data =f"tanzania {file_id}"),
                                    InlineKeyboardButton("🇰🇪 KENYA",callback_data ="kenya" )
                                ]
                            ]
                        )
                    )
                return
            await akg.delete()
            strg=files.descp.split('.dd#.')[3]
            if filedetails:
                if filedetails:
                    if strg.lower() == 'm':
                        filez=await get_filter_results(file_id,group_id)
                        for file in reversed(filez):
                            filedetails = await get_file_details(file.id)
                            for files in filedetails:
                                f_caption=files.reply
                                await client.send_cached_media(
                                    chat_id=cmd.from_user.id,
                                    file_id=files.file,
                                    caption=f_caption
                                )
                        return
                    elif strg.lower() == 's':
                        link = files.descp.split('.dd#.')[2]
                        f_caption =f'\n🌟 @Bandolako2bot \n\n **💥Series  zetu zote zipo google drive, Kama huwezi kufungua link zetu tafadhali bonyeza 📪 ADD EMAIL kisha fuata maelekezo**'
                        await client.send_photo(
                            chat_id=cmd.from_user.id,
                            photo=files.file,
                            caption=f_caption,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📪 ADD EMAIL",callback_data = "addemail")],[InlineKeyboardButton("🔗 GOOGLE LINK",url= link)]])
                        )
                        return
                     
                else:
                    await client.send_message(
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
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):
        if query.data == "kundii":
            await query.edit_message_text(text = "🌺🌺🌺🌺🌺🌺🌺🌺🌺\nTafaddali chagua kundi la kusahihisha au bonyeza add group kuongeza kundi jengine\n\n🌸kisha subiri utapewa maelekezo jinsi ya kusahihisha kundi lako\n\n💥Kumbuka makundi mwisho ni sita tu , pangilia vizuri makundi yako", 
                reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(text = 'Add group ', callback_data = 'adgrp')
                    ]]))
            await query.answer('hellow')
        elif query.data == "adgrp":
            await query.answer('Subiri kidogo')
            await query.message.delete()
            mkv = await client.ask(text='hllowe',chat_id = query.from_user.id,reply_markup=ForceReply())
        elif query.data == "aina":
            await query.answer('hi')

        elif query.data == "startup":
            await query.answer('mambo')

        elif query.data == "namba":
            await query.answer('vp')

        elif query.data == "kenya":
            await query.answer()
            mkv = await client.ask(text = " Samahani sana wateja wetu wa Kenya bado hatuja weka utaratibu mzuri.\n  hivi karibun tutaweka mfumo mzuri ili muweze kupata huduma zetu", chat_id = query.from_user.id)
        
        elif query.data.startswith("tanzania"):
            await query.answer()
            fileid = query.data.split(" ",1)[1]
            await query.message.delete()
            filedetails = await get_file_details(fileid)
            id3=fileid
            for files in filedetails:
                f_caption=files.reply
                group_id = files.group_id
                fileid = files.file
                type1 = files.type
            db_details = await db.get_db_status(group_id)
            if type1=="Photo":
                await client.send_photo(
                            chat_id=query.from_user.id,
                            photo= fileid,
                            caption =f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA {db_details.db_name.upper()} ** \nTafadhali chagua kifurush kupata maelezo zaidi na jinsi ya kufanya malipo kwa kubonyeza button zilizopo chini\n **__KARIBUN SANA {db_details.db_name.upper()} __**',
                            reply_markup=InlineKeyboardMarkup([replymkup1(db_details.g_1,fileid,g_1),replymkup1(db_details.g_2,fileid,g_2),replymkup1(db_details.g_3,fileid,g_3),replymkup1(db_details.g_4,fileid,g_4),replymkup1(db_details.g_5,fileid,g_5),replymkup1(db_details.g_6,fileid,g_6),[InlineKeyboardButton("Lipia hii __ tu", callback_data=f"wik2 {fileid}.g_1.500.m")]]) )
            else:
                await client.send_cached_media(
                                    chat_id=query.from_user.id,
                                    file_id=fileid,
                                    caption =f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA {db_details.db_name.upper()} ** \nTafadhali chagua kifurush kupata maelezo zaidi na jinsi ya kufanya malipo kwa kubonyeza button zilizopo chini\n **__KARIBUN SANA {db_details.db_name.upper()} __**',
                                    reply_markup=InlineKeyboardMarkup([replymkup1(db_details.g_1,fileid,g_1),replymkup1(db_details.g_2,fileid,g_2),replymkup1(db_details.g_3,fileid,g_3),replymkup1(db_details.g_4,fileid,g_4),replymkup1(db_details.g_5,fileid,g_5),replymkup1(db_details.g_6,fileid,g_6),[InlineKeyboardButton("Lipia hii __ tu", callback_data=f"wik2 {fileid}.g_1.500.m")]]) )
            
        elif query.data.startswith("wik"):
            await query.answer()
            fileid,msg2 = query.split(" ")[1].split(".")
            filedetails = await get_file_details(fileid)
            await query.message.delete()
            for files in filedetails:
                group_id = files.group_id
            msg1 = group_id
            details = await get_db_status(msg1)
            data1= details.msg2
            data2= data1.split(" ")[1]
            await client.send_message(chat_id = query.from_user.id,text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{data1.split(' ')[0]}\n {data1.split(' ')[2]}\n Tafadhali bonyeza kitufe hapo chini kuweza kulipia muda utakao weza kupata huduma hii",
                    reply_markup=InlineKeyboardMarkup([replymkup2(f"week 1 tsh {data2.split(',')[0]}",f"{fileid}.{msg2}.{data2.split(',')[0]}.wk1"),replymkup2(f"week 2 tsh {data2.split(',')[1]}",f"{fileid}.{msg2}.{data2.split(',')[1]}.wk2"),replymkup2(f"week 3 tsh {data2.split(',')[2]}",f"{fileid}.{msg2}.{data2.split(',')[2]}.wk3"),replymkup2(f"mwezi 1 tsh {data2.split(',')[3]}",f"{fileid}.{msg2}.{data2.split(',')[3]}.mwz1"),[InlineKeyboardButton("rudi mwanzo", callback_data=f"tanzania {fileid}")]])
                )
        elif query.data.startswith("wik2"):
            await query.answer()
            fileid,msg2,prc1,tme = query.split(" ")[1].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.file_name
                grp = files.grp
            details = await get_db_status(group_id)
            data1 = details.msg2
            if tme=="wk1":
                tme1= "wiki 1"
            elif tme=="wk2":
                tme1= "wiki 2"
            elif tme=="wk3":
                tme1= "wiki 3"
            elif tme== "mwz1":
                tme1= "mwezi mmoja"
            else:
                tme1=tme
            data2 = data1.split(" ")[0]
            p1,p2,p3 =details.phone_no.split(" ")
            mda = details.muda
            if tme == "m":
                await query.edit_message_text(
                        text = f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details.dbname.upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc2} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p3} \nKumbuka unalipia tsh {prc2} kwa ajili ya kununua  {grp} ya {name} {mda} \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data="malipo {query.split(" ")[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                    )
            else:
                await query.edit_message_text(
                        text = f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details.dbname.upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc1} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p3} \nKumbuka unalipia tsh {prc1} kupata huduma ya {data2} kwa muda wa {tme1} bila kuzuiwa kutopata huduma hii \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data="malipo {query.split(' ')[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                    )
        elif query.data.startswith("malipo"):
            await query.answer()
            fileid,msg2,prc1,tme = query.split(" ")[1].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.file_name
                grp = files.grp
            if tme=="wk1":
                tme1= "wiki 1"
            elif tme=="wk2":
                tme1= "wiki 2"
            elif tme=="wk3":
                tme1= "wiki 3"
            elif tme== "mwz1":
                tme1= "mwezi mmoja"
            else:
                tme1=tme
            details = await get_db_status(group_id)
            data1 = details.msg2
            p1,p2,p3 =details.phone_no.split(" ")
            mda = details.muda
            mkv = await client.ask(text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\nTuma screenshot ya malipo yako kisha subir kidogo wasimamiz wangu wahakiki muamala wako',chat_id = query.from_user.id,reply_markup=ForceReply())
            if mkv.photo:
                await query.message.delete()
                await client.send_message(chat_id = query.from_user.id,text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\ntumepokea screenshot ngoja tuihakiki tutakupa majibu tukimaliza')
                if tme=='m':
                    await client.send_photo(
                            chat_id=int(group_id),
                            photo= mkv.photo.file_id,
                            caption = f'Mteja [{query.from_user.first_name}](tg://user?id={query.from_user.id})Amechagua \n Jina :{name}\nAina : {grp}\nBei yake : Tsh {prc2} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {grp} hii,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"yes {query.from_user.id} {query.split(' ')[1]}@#{query.from_user.first_name}"),InlineKeyboardButton("chat private", url=f"tg://user?id={query.from_user.id}")]]))
                else:
                    await client.send_photo(
                            chat_id=int(group_id),
                            photo= mkv.photo.file_id,
                            caption = f'Mteja [{query.from_user.first_name}](tg://user?id={query.from_user.id})Amechagua \n {data1.split(" ")[1].upper()}\n kifurushi : {tme1}\nBei yake : Tsh {prc1} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {data1.split(" ")[1].upper()} ,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"yes {query.from_user.id} {query.split(' ')[1]}@#{query.from_user.first_name}"),InlineKeyboardButton("chat private", url=f"tg://user?id={query.from_user.id}")]]))
                
            else:
                await mkv.delete()
                if tme == "m":
                     await query.edit_message_text(
                            text = f'NMELAZIMIKA KUKURUDISHA HAPA \n(tafadhali Fanya kwa usahihi kama unavyo ambiwa kama huwez omba msaada usaidiwe)🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details.dbname.upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc2} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p2} \nKumbuka unalipia tsh {prc2} kwa ajili ya kununua  {grp} ya {name} {mda} \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data="malipo {query.split(' ')[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                        )
                else:
                    await query.edit_message_text(
                            text = f'NMELAZIMIKA KUKURUDISHA HAPA \n(tafadhali Fanya kwa usahihi kama unavyo ambiwa kama huwez omba msaada usaidiwe)🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details.dbname.upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc1} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p3} \nKumbuka unalipia tsh {prc1} kupata huduma ya {data2} kwa muda wa {tme1} bila kuzuiwa kutopata huduma hii \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data="malipo {query.split(' ')[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                       )
        elif query.data.startswith("yes"):
            msg1 = query.split(" ")[1]
            msg2 = query.split(" ")[2].split("@#")[1]
            await query.edit_message_caption(
                    caption = f'je unauhakika tumruhusu [{msg2}](tg://user?id={int(msg1)}) bonyeza ndiyo kukubali au bonyeza rudi kurudi kupata maelezo ya muamala',
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ndiyo", callback_data=f"ndiyo {msg1} {query.data.split(' ')[2]}"),InlineKeyboardButton("rudi ", callback_data=f"rudi {msg1} {query.data.split(' ')[2]}")]])
                )
        elif query.data.startswith("rudi"):
            msg,msg1,data3 = query.split(" ")         
            msg3 = data3.split("@#")[1]
            fileid,msg2,prc1,tme = data3.split("@#")[0].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.file_name
                grp = files.grp
            if tme=="wk1":
                tme1= "wiki 1"
            elif tme=="wk2":
                tme1= "wiki 2"
            elif tme=="wk3":
                tme1= "wiki 3"
            elif tme== "mwz1":
                tme1= "mwezi mmoja"
            else:
                tme1=tme
            details = await get_db_status(group_id)
            data1 = details.msg2
            if tme1=="m":
                await query.edit_message_caption(
                        caption = f'Mteja [{msg3}](tg://user?id={int(msg1)})Amechagua \n Jina :{name}\nAina : {grp}\nBei yake : Tsh {prc2} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {grp} hii,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"yes {msg1} {data3}"),InlineKeyboardButton("chat private", url=f"tg://user?id={int(msg1)}")]])
                    )
            else:
                await query.edit_message_caption(
                        caption = f'Mteja [{msg3}](tg://user?id={int(msg1)})Amechagua \n {data1.split(" ")[1].upper()}\n kifurushi : {tme1}\nBei yake : Tsh {prc1} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {data1.split(" ")[1].upper()} ,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"yes {msg1} {data3}"),InlineKeyboardButton("chat private", url=f"tg://user?id={int(msg1)}")]])
                    )
        elif query.data.startswith("ndiyo"):
            msg,msg1,data3 = query.split(" ")         
            msg3 = data3.split("@#")[1]
            fileid,msg2,prc1,tme = data3.split("@#")[0].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.file_name
                grp = files.grp
            if tme=="wk1":
                tme1= 7
            elif tme=="wk2":
                tme1= 14
            elif tme=="wk3":
                tme1= 21
            elif tme== "mwz1":
                tme1= 30
            if tme == "m":
                await db.add_acc(id,msg1,fileid,query.from_user.id,999)
            else:
                await db.add_acc(id,msg1,msg2,query.from_user.id,tme1)
            await client.send_message(chat_id = query.from_user.id,text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿 mteja {msg3} amesharuhusiwa kupata huduma ya kifurush alicho chagua Asante kwa mda wako"
                    )
            await client.send_message(chat_id = int(msg1),text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿Samahani kwa kukuchelewesha kukuruhusu mapema ila tutajitahidi kuboresha huduma zetu,Kwa sasa unaweza kupata huduma uliyoomba\n\n kujua salio na vifurushi vyako vyote tuma neno salio ukiwa private yaani kwenye bot."
                    )
        elif query.data.startswith("0"):
            msg1=query.split(" ")[1]
            msg0=query.split(" ")[0]
            if msg0=="0":
                msg0="0"
            else:
                msg0+="0"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
            if msg0=="0":
                msg0="0"
            else:
                msg0+="00"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("000"):
            
            msg1=query.split(" ")[1]
            msg0=query.split(" ")[2]
            if msg0=="0":
                msg0="0"
            else:
                msg0+="000"
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} {msg0}',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
        elif query.data.startswith("delete"):
            
            msg1=query.split(" ")[1]
            await query.edit_message_text(
                    text = f'{query.message.text}\n{msg1} 0',
                    reply_markup = InlineKeyboardMarkup([[]]),
                )
def replymkup(msg7,txt1):
    reply1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1", callback_data="1 msg7 txt1"),
                InlineKeyboardButton("2", callback_data="2 msg7 txt1"),
                InlineKeyboardButton("3", callback_data="3 msg7 txt1"),
                InlineKeyboardButton("4", callback_data="4 msg7 txt1"),
                InlineKeyboardButton("5", callback_data="5 msg7 txt1")
            ],
            [
                InlineKeyboardButton("6", callback_data="6 msg7 txt1"),
                InlineKeyboardButton("7", callback_data="7 msg7 txt1"),
                InlineKeyboardButton("8", callback_data="8 msg7 txt1"),
                InlineKeyboardButton("9", callback_data="9 msg7 txt1"),
                InlineKeyboardButton("0", callback_data="0 msg7 txt1")
            ],
            [
                InlineKeyboardButton("00", callback_data="00 msg7 txt1"),
                InlineKeyboardButton("000", callback_data="000 msg7 txt1"),
                InlineKeyboardButton("✅", callback_data="upl msg7 txt1"),
                InlineKeyboardButton("❎", callback_data="del msg7 txt1")
            ]

        ])
def replymkup2(msg2,msg4):
    msg1 = msg2.split('tsh ')[1]
    if msg1 == 0:
        return []
    else:
        return [InlineKeyboardButton(f"{msg2}", callback_data="wik2 msg4")]

def replymkup1(msg3,msg1,msg2):
    if msg3=="hrm45":
        return []
    else:
        msg3=msg3.split(" ")[0]
        return [InlineKeyboardButton(f"{msg3}", callback_data=f"wik {msg1}.{msg2}")]
