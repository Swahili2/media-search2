from info import filters
import uuid
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
            reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('Rekebisha Makundi', callback_data = "kundii")],[InlineKeyboardButton('Rekebisha Aina', callback_data = "aina")],[InlineKeyboardButton('Rekebisha Jina la Kikundi', callback_data = "dbname")],[InlineKeyboardButton('Rekebisha Startup sms', callback_data = "startup")],[InlineKeyboardButton('Rekebisha Mawasiliano', callback_data = "xba")]])
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
                id2 = files.id
                group_id = files.group_id
                grp = files.grp
            ban_status = await db.get_ban_status(group_id)    
            if ban_status["is_banned"] == False:
                await client.send_message(
                        chat_id=cmd.from_user.id,
                        text=f"Samahani **{cmd.from_user.first_name}** nmeshindwa kukuruhusu kendelea kwa sababu Kifurushi admin alicho lipia kimeisha mtaarifu alipie bonyeza maneno ya blue \n[ADMIN](tg://user?id={group_id})\n\nIli muweze kuendelea kumutumia robot huyu",
            if not (await db.is_acc_exist(cmd.from_user.id,grp,group_id) or await db.is_acc_exist(cmd.from_user.id,id2,group_id) or group_id == cmd.from_user.id) :
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
            ab = await db.get_db_status(query.from_user.id)
            grp="grp"
            if ab['g_1']=="hrm45":
                reply_markup=replymkup3(ab,grp,1)
            elif ab['g_2']=="hrm45":
                reply_markup=replymkup3(ab,grp,2)
           
            elif ab['g_3']=="hrm45":
                reply_markup=replymkup3(ab,grp,3)
            elif ab['g_4']=="hrm45":
                reply_markup=replymkup3(ab,grp,4)
            elif ab['g_5']=="hrm45":
                reply_markup=replymkup3(ab,grp,5)
            elif ab['g_6']=="hrm45":
                reply_markup=replymkup3(ab,grp,6)
            else:
                reply_markup=replymkup3(ab,grp,7)
            await query.edit_message_text(text = "🌺🌺🌺🌺🌺🌺🌺🌺🌺\nTafadhali chagua kundi la kusahihisha au bonyeza 🦋 ADD KIFURUSHI kuongeza kifurushi kingine\n\n🌸kisha subiri utapewa maelekezo jinsi ya kusahihisha kundi lako\n\n💥Kumbuka makundi mwisho ni sita tu , pangilia vizuri makundi yako", 
                reply_markup=reply_markup)
            await query.answer('Tafadhali subiri')
        elif query.data.startswith("adgrp"):
            await query.answer('Subiri kidogo')
            await query.message.delete()
            ab = await db.get_db_status(query.from_user.id)
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\nTafadhali tuma jina la kifurushi kipya bei ya wiki wiki2 wiki3 au mwezi kisha maelezo kidogo ya huduma hii zikitenganishwa na #@\n\n💫Mfano1 kifurushi cha vyote#@5000@6000#@7000#@8000#@Unaeza ukapata huduma zote ikiwemo series movies n.k\n\n💫Mfano2 kifurushi cha singo #@2000#@0#@0#@5000#@hapa utajipatia singo zilizotafsiriwa na ambazo hazijatafsiriwa tu \n\n💫Mfano3 Kifurushi cha tamthilia#@3500#@6000#@0#@8000#@hapa utajipatia tamthilia Kali ikiwemo huba\n\n⚡️Kumbuka ukiweka bei ni 0 hicho kipengele hakitakuepo kwenye kuonyesha bei za wiki za vifurush Vyako kwa wateja :💫mfano3 utaonyesha bei za wiki1,wik2,mwez. Ila wiki3 haitaonyesha',chat_id = query.from_user.id,reply_markup=ForceReply())
            try:
                mkv1,mkv2,mkv3,mkv4,mkv5,mkv6=mkv.text.split("#@")
                int(mkv5)
                int(mkv2)
                int(mkv3)
                int(mkv4)
            except:
                await mkv.delete()
                await client.send_message(chat_id = query.from_user.id,text=f"umetuma ujumbe ambao s sahihi,Kama hujaelewa jinsi kuandika tafadhal mcheki msimamiz @hrm45 akusaidie bonyeza rudi nyuma uanze upya kutengeneza kifurushii",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'kundii')]]))
                return
            ghi1=query.data.split(" ")[1]
            ghi=f"{ghi1} {mkv1}#@{mkv2},{mkv3},{mkv4},{mkv5}#@{mkv6}"
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data added successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'kundii')]]))
                
        elif query.data.startswith("ad2grp"):
            await query.answer('Subiri kidogo')
            await query.message.delete()
            ghi1=query.data.split(" ")[1]
            mkv = await client.ask(text=f'⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\nTafadhali tuma jina wakilisikisha bei ya wiki wiki2 wiki3 au mwezi kisha maelezo kidogo ya huduma hii zikitenganishwa na #@\n\n💫Mfano1 kifurushi cha vyote#@5000@6000#@7000#@8000#@Unaeza ukapata huduma zote ikiwemo series movies n.k\n\n💫Mfano3 Kifurushi cha tamthilia#@3500#@6000#@0#@8000#@hapa utajipatia tamthilia Kali ikiwemo huba\n\n⚡️Kumbuka ukiweka bei ni 0 hicho kipengele hakitakuepo kwenye orodha kuonyesha bei za wiki za vifurush Vyako kwa wateja :💫mfano3 utaonyesha bei za wiki1,wik2,mwez. Ila wiki3 haitaonyesha\n\nNote aina zote za media za mwanzo zilizotumia kifurushi hiki unachotaka kubadilisha,zitabadilika kutumia jina hili jipya utakalotupa',chat_id = query.from_user.id,reply_markup=ForceReply())
            ab = await db.get_db_status(query.from_user.id)
            try:
                mkv1,mkv2,mkv3,mkv4,mkv5,mkv6=mkv.text.split("#@")
                int(mkv5)
                int(mkv2)
                int(mkv3)
                int(mkv4)
            except:
                await mkv.delete()
                await client.send_message(chat_id = query.from_user.id,text=f"umetuma ujumbe ambao s sahihi,Kama hujaelewa jinsi tafadhal mcheki msimamiz @hrm45 akusaidie bonyeza rudi nyuma uanze upya kutengeneza kifurushi",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'kundii')]]))
                return
            
            ghi=f"{ghi1} {mkv1}#@{mkv2},{mkv3},{mkv4},{mkv5}#@{mkv6}"
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data updated successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'kundii')]]))
                
        elif query.data == "aina":
            await query.answer('Tafadhali subiri kidogo')
            ab = await db.get_db_status(query.from_user.id)
            ab1,ab2,ab3,ab4,ab5,ab6,ab7,ab8,ab9,ab10=ab["aina"].split("#@#")
            ain="ain"
            if ab1=="hrm45":
                reply_markup=replymkup3(ab,ain,1)
            elif ab2=="hrm45":
                reply_markup=replymkup3(ab,ain,2)
            elif ab3=="hrm45":
                reply_markup=replymkup3(ab,ain,3)
            elif ab4=="hrm45":
                reply_markup=replymkup3(ab,ain,4)
            elif ab5=="hrm45":
                reply_markup=replymkup3(ab,ain,5)
            elif ab6=="hrm45":
                reply_markup=replymkup3(ab,ain,6)
            elif ab7=="hrm45":
                reply_markup=replymkup3(ab,ain,7)
            elif ab8=="hrm45":
                reply_markup=replymkup3(ab,ain,8)
            elif ab9=="hrm45":
                reply_markup=replymkup3(ab,ain,9)
            elif ab10=="hrm45":
                reply_markup=replymkup3(ab,ain,10)
            else:
                reply_markup=replymkup3(ab,ain,11)
            await query.edit_message_text(text = "🌺🌺🌺🌺🌺🌺🌺🌺🌺\nTafadhali chagua aina ya media zako kusahihisha au bonyeza 🦋 ONGEZA AINA kuongeza aina kingine\n\n🌸kisha subiri utapewa maelekezo jinsi ya kusahihisha kundi lako\n\n💥Kumbuka aina mwisho ni kumi tu , pangilia vizuri aina zako", 
                reply_markup=reply_markup)
        elif query.data.startswith("adain"):
            await query.answer('Subiri kidogo')
            await query.message.delete()
            ab = await db.get_db_status(query.from_user.id)
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ ',chat_id = query.from_user.id,reply_markup=ForceReply())
            if mkv.text==None:
                await client.send_message(chat_id = query.from_user.id,text=f"umetuma ujumbe ambao s sahihi,Kama hujaelewa jinsi kuandika tafadhal mcheki msimamiz @hrm45 akusaidie bonyeza rudi nyuma uanze upya kutengeneza aina za media zako",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'aina')]]))
                return
            ghi1=ab["aina"].split("#@#")
            ghi2 = int(query.data.split(" ")[1])
            ghi = 'aina '
            for i in range(0,10):
                ghi3=ghi1[i]
                if i == ghi2:
                    ghi3 = mkv.text
                if i == 0:
                    ghi=f'{ghi}{ghi3}'
                else:
                    ghi=f'{ghi}#@#{ghi3}'
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data added successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'aina')]]))
                
        elif query.data.startswith("ada2in"):
            await query.answer('Subiri kidogo')
            await query.message.delete()
            ab = await db.get_db_status(query.from_user.id)
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️ wakilish',chat_id = query.from_user.id,reply_markup=ForceReply())
            if mkv.text==None:
                await client.send_message(chat_id = query.from_user.id,text=f"umetuma ujumbe ambao s sahihi,Kama hujaelewa jinsi kuandika tafadhal mcheki msimamiz @hrm45 akusaidie bonyeza rudi nyuma uanze upya kutengeneza aina za media zako",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'aina')]]))
                return
            ghi1=ab["aina"].split("#@#")
            ghi2 = int(query.data.split(" ")[1])
            ghi = 'aina '
            for i in range(0,10):
                ghi3=ghi1[i]
                if i == ghi2:
                    ghi3 = mkv.text
                if i == 0:
                    ghi=f'{ghi}{ghi3}'
                else:
                    ghi=f'{ghi}#@#{ghi3}'
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data updated successful l",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'aina')]]))
                
        elif query.data == "startup":
            await query.answer('uzuri wa kitu ni muonekano')
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\nTafadhali Tuma maelezo kidogo kuhusu huduma/biashara unayo Fanya .Haya maelezo yataonekana endapo Mteja wako atakapo anza kumtumia robot huyu,\nKumbuka pia ukituma ujumbe wa zamani unafutwa kama ulishwahi tuma\n\nkwa maelezo zaidi mxheki @hrm45 akuelekeze zaidi',chat_id = query.from_user.id,reply_markup=ForceReply())
            ghi=f'descp {mkv.text}'
            ab = await db.get_db_status(query.from_user.id)
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data updated successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'zkb')]]))
                
        elif query.data == "xba":
            await query.answer('Mandao pendwa ndio bora')
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\nTafadhali Tuma namba kisha acha nafasi kampuni mfano 062466xxxx halopesa/nkumbuka namba ianze na 0 sio +255',chat_id = query.from_user.id,reply_markup=ForceReply())
            try:
                 int(mkv.text.split(" ")[0])
            except:
                await mkv.delete()
                await client.send_message(chat_id = query.from_user.id,text=f"umetuma ujumbe ambao s sahihi,Kama hujaelewa jinsi tafadhal mcheki msimamiz @hrm45 akusaidie bonyeza rudi nyuma uanze upya kutengeneza namba ya miamala yako",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'zkb')]]))
                return
            ghi=f'phone_no {mkv.text}'
            ab = await db.get_db_status(query.from_user.id)
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data updated successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'zkb')]]))
            
        elif query.data == "dbname":
            await query.answer('jina zuri huonesha uzuri')
            mkv = await client.ask(text='⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️\nTafadhali tuma jina la kikundi chako Mfano Swahili media group au Baoflix movies n.k ',chat_id = query.from_user.id,reply_markup=ForceReply())
            ghi=f'dbname {mkv.text}'
            ab = await db.get_db_status(query.from_user.id)
            await db.update_db(query.from_user.id,ghi,ab)
            await mkv.reply_text(text=f"data updated successful ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = f'rudi nyuma' , callback_data = 'zkb')]]))
                
        elif query.data == "kenya":
            await query.answer()
            
        elif query.data.startswith("tanzania"):
            await query.answer()
            fileid = query.data.split(" ",1)[1]
            await query.message.delete()
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                f_caption=files.reply
                group_id = files.group_id
                id3 = files.file
                type1 = files.type
            db_details = await db.get_db_status(group_id)
            if type1=="Photo":
                await client.send_photo(
                            chat_id=query.from_user.id,
                            photo= id3,
                            caption =f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA {db_details["db_name"].upper()} ** \nTafadhali chagua kifurush kupata maelezo zaidi na jinsi ya kufanya malipo kwa kubonyeza button zilizopo chini\n **__KARIBUN SANA {db_details["db_name"].upper()} __**',
                            reply_markup=InlineKeyboardMarkup([replymkup1(db_details["g_1"],fileid,'g_1'),replymkup1(db_details["g_2"],fileid,'g_2'),replymkup1(db_details["g_3"],fileid,'g_3'),replymkup1(db_details["g_4"],fileid,'g_4'),replymkup1(db_details["g_5"],fileid,'g_5'),replymkup1(db_details["g_6"],fileid,'g_6'),[InlineKeyboardButton("Lipia hii __ tu", callback_data=f"wiik2 {fileid}.g_1.500.m")]]) )
            else:
                await client.send_cached_media(
                                    chat_id=query.from_user.id,
                                    file_id=id3,
                                    caption =f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n** VIFURUSHI VYA {db_details["db_name"].upper()} ** \nTafadhali chagua kifurush kupata maelezo zaidi na jinsi ya kufanya malipo kwa kubonyeza button zilizopo chini\n **__KARIBUN SANA {db_details["db_name"].upper()} __**',
                                    reply_markup=InlineKeyboardMarkup([replymkup1(db_details["g_1"],fileid,'g_1'),replymkup1(db_details["g_2"],fileid,'g_2'),replymkup1(db_details["g_3"],fileid,'g_3'),replymkup1(db_details["g_4"],fileid,'g_4'),replymkup1(db_details["g_5"],fileid,'g_5'),replymkup1(db_details["g_6"],fileid,'g_6'),[InlineKeyboardButton("Lipia hii __ tu", callback_data=f"wiik2 {fileid}.g_1.500.m")]]) )
           
        elif query.data.startswith("wik"):
            await query.answer()
            msgg1,fileid,msg2=query.data.split(" ") 
            filedetails = await get_file_details(fileid)
            await query.message.delete()
            for files in filedetails:
                group_id = files.group_id
            msg1 = group_id
            details = await db.get_db_status(msg1)
            data1= details[msg2]
            data2= data1.split("#@")[1]
            await client.send_message(chat_id = query.from_user.id,text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{data1.split('#@')[0]}\n {data1.split('#@')[2]}\n Tafadhali bonyeza kitufe hapo chini kuweza kulipia muda utakao weza kupata huduma hii",
                    reply_markup=InlineKeyboardMarkup([replymkup2(f"week 1 tsh {data2.split(',')[0]}",f"{fileid}.{msg2}.{data2.split(',')[0]}.wk1"),replymkup2(f"week 2 tsh {data2.split(',')[1]}",f"{fileid}.{msg2}.{data2.split(',')[1]}.wk2"),replymkup2(f"week 3 tsh {data2.split(',')[2]}",f"{fileid}.{msg2}.{data2.split(',')[2]}.wk3"),replymkup2(f"mwezi 1 tsh {data2.split(',')[3]}",f"{fileid}.{msg2}.{data2.split(',')[3]}.mwz1"),[InlineKeyboardButton("rudi mwanzo", callback_data=f"tanzania {fileid}")]])
                )
        elif query.data.startswith("wiik2"):
            await query.answer()
            fileid,msg2,prc1,tme = query.data.split(" ")[1].split(".")
            filedetails = await get_file_details(fileid)

            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.text.split('.dd#.',1)[0]
                grp = files.grp
            details = await db.get_db_status(group_id)
            data1 = details[msg2]
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
            data2 = data1.split("#@")[0]
            p1,p2,p3 =details["phone_no"].split(" ")
            mda = details["muda"]
            if tme == "m":
                await query.edit_message_text(
                        text = f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details["db_name"].upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc2} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p3} \nKumbuka unalipia tsh {prc2} kwa ajili ya kununua  {grp} ya {name} {mda} \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data=f"malipo {query.data.split(' ')[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                    )
            else:
                await query.edit_message_text(
                        text = f'🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\n{details["db_name"].upper} PAYMENT SECTION \nTafadhali lipia\n Tsh {prc1} kwenda \nNo : {p1}\nKampuni : {p3}\nJina : {p3} \nKumbuka unalipia tsh {prc1} kupata huduma ya {data2} kwa muda wa siku {tme1} bila kuzuiwa kutopata huduma hii \n\nUkishafanya  malipo bonyeza button nmeshafanya malipo kisha tuma screenshot ya malipo/muamala',
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("nmeshafanya malipo", callback_data=f"malipo {query.data.split(' ')[1]}"),InlineKeyboardButton("rudi mwanzo ", callback_data=f"tanzania {fileid}")]]),
                    )
        elif query.data.startswith("malipo"):
            await query.answer()
            fileid,msg2,prc1,tme = query.data.split(" ")[1].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.text.split('.dd#.',1)[0]
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
            details = await db.get_db_status(group_id)
            data1 = details[msg2]
            p1,p2,p3 =details['phone_no'].split(" ")
            mda = details['muda']
            mkv = await client.ask(text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\nTuma screenshot ya malipo yako kisha subir kidogo wasimamiz wangu wahakiki muamala wako',chat_id = query.from_user.id,reply_markup=ForceReply())
            if mkv.photo:
                await query.message.delete()
                await client.send_message(chat_id = query.from_user.id,text='🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿\ntumepokea screenshot ngoja tuihakiki tutakupa majibu tukimaliza')
                if tme=='m':
                    await client.send_photo(
                            chat_id=int(group_id),
                            photo= mkv.photo.file_id,
                            caption = f'Mteja [{query.from_user.first_name}](tg://user?id={query.from_user.id})Amechagua \n Jina :{name}\nAina : {grp}\nBei yake : Tsh {prc2} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {grp} hii,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"y {query.from_user.id} {query.data.split(' ')[1]}"),InlineKeyboardButton("chat private", url=f"tg://user?id={query.from_user.id}")]]))
                else:
                    await client.send_photo(
                            chat_id=int(group_id),
                            photo= mkv.photo.file_id,
                            caption = f'Mteja [{query.from_user.first_name}](tg://user?id={query.from_user.id})Amechagua \n {data1.split(" ")[1].upper()}\n kifurushi : {tme1}\nBei yake : Tsh {prc1} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {data1.split(" ")[1].upper()} ,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"y {query.from_user.id} {query.data.split(' ')[1]}"),InlineKeyboardButton("chat private", url=f"tg://user?id={query.from_user.id}")]]))
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
            
        elif query.data.startswith("y"):
            msg1 = query.data.split(" ")[1]
            #msg2 = query.data.split(" ")[2].split("@#")[1]
            await query.edit_message_caption(
                    caption = f'je unauhakika tumruhusu [{msg1}](tg://user?id={int(msg1)}) bonyeza ndiyo kukubali au bonyeza rudi kurudi kupata maelezo ya muamala',
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ndiyo", callback_data=f"n {msg1} {query.data.split(' ')[2]}"),InlineKeyboardButton("rudi ", callback_data=f"r {msg1} {query.data.split(' ')[2]}")]])
                )
        elif query.data.startswith("r"):
            msg,msg1,data3 = query.data.split(" ")         
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
            details = await db.get_db_status(group_id)
            data1 = details.msg2
            if tme1=="m":
                await query.edit_message_caption(
                        caption = f'Mteja [{msg1}](tg://user?id={int(msg1)})Amechagua \n Jina :{name}\nAina : {grp}\nBei yake : Tsh {prc2} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {grp} hii,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"y {msg1} {data3}"),InlineKeyboardButton("chat private", url=f"tg://user?id={int(msg1)}")]])
                    )
            else:
                await query.edit_message_caption(
                        caption = f'Mteja [{msg1}](tg://user?id={int(msg1)})Amechagua \n {data1.split(" ")[1].upper()}\n kifurushi : {tme1}\nBei yake : Tsh {prc1} \nTafadhal hakiki huu muamala wake,Kama amekosea tafadhal bonyeza chat private au maneno ya blue yaani jina lake kisha muelekeze aanze upya kuchagua kifurush sahihi au kutuma screenshot ya muamala sahihi.\n Bonyeza activate kumruhusu aweze kupata huduma ya {data1.split(" ")[1].upper()} ,Kama muamala wake upo sahihi \n\nNote:Kama utamshauri aanze upya tafadhali futa huu ujumbe ili usichanganye mada(ushauri tu)' ,
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Activate", callback_data=f"y {msg1} {data3}"),InlineKeyboardButton("chat private", url=f"tg://user?id={int(msg1)}")]])
                    )
        elif query.data.startswith("n"):
            msg,msg1,data3 = query.data.split(" ")         
            fileid,msg2,prc1,tme = data3.split("@#")[0].split(".")
            filedetails = await get_file_details(fileid)
            for files in filedetails:
                group_id = files.group_id
                prc2 = files.price
                name = files.text.split('.dd#.',1)[0]
                grp = files.grp
            if tme=="wk1":
                tme1= 7
            elif tme=="wk2":
                tme1= 14
            elif tme=="wk3":
                tme1= 21
            elif tme== "mwz1":
                tme1= 30
            strid = str(uuid.uuid4())
            if tme == "m":
                await db.add_acc(strid,msg1,fileid,query.from_user.id,999)
            else:
                await db.add_acc(strid,msg1,msg2,query.from_user.id,tme1)
            await client.send_message(chat_id = query.from_user.id,text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿 mteja [{msg1}](tg://user?id={int(msg1)}) amesharuhusiwa kupata huduma ya kifurush alicho chagua Asante kwa mda wako"
                    )
            await client.send_message(chat_id = int(msg1),text=f"🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿🇹🇿Samahani kwa kukuchelewesha kukuruhusu mapema ila tutajitahidi kuboresha huduma zetu,Kwa sasa unaweza kupata huduma uliyoomba\n\n kujua salio na vifurushi vyako vyote tuma neno salio ukiwa private yaani kwenye bot."
                    )
        
        elif query.data.startswith("zkb"):
            await query.edit_message_text(text="chagua huduma unayotaka kufanya marekebisho",
                reply_markup =InlineKeyboardMarkup([[InlineKeyboardButton('Rekebisha Makundi', callback_data = "kundii")],[InlineKeyboardButton('Rekebisha Aina', callback_data = "aina")],[InlineKeyboardButton('Rekebisha Jina la Kikundi', callback_data = "dbname")],[InlineKeyboardButton('Rekebisha Startup sms', callback_data = "startup")],[InlineKeyboardButton('Rekebisha Mawasiliano', callback_data = "xba")]])
            )
def replymkup2(msg2,msg4):
    msg1 = msg2.split('tsh ')[1]
    if msg1 == 0:
        return []
    else:
        return [InlineKeyboardButton(f"{msg2}", callback_data=f"wiik2 {msg4}")]

def replymkup1(msg3,msg1,msg2):
    if msg3=="hrm45":
        return []
    else:
        msg3=msg3.split("#@")[0]
        return [InlineKeyboardButton(f"{msg3}", callback_data=f"wik {msg1} {msg2}")]
def replymkup3(ab,typ,nmb):
    ab3=[]
    for i in range(0,nmb):
        if typ=="grp":
            if i == (nmb-1) and i !=6 :
                b=i+1
                ab2 = [InlineKeyboardButton(text = '🦋 ADD KIFURUSHI ', callback_data = f'adgrp g_{b}')]
                ab3.append(ab2)    
            elif i != 6:
                a=i+1
                abh=f'g_{a}'
                ab1=ab[abh].split("#@")[0]
                ab2=[InlineKeyboardButton(text = f'🦋 {ab1}' , callback_data = f'ad2grp {abh}')]
                ab3.append(ab2)
        elif typ=="ain":
            if i == (nmb-1) and i != 10 :
                ab1=ab["aina"].split('#@#')[i]
                ab2=[InlineKeyboardButton(text = f'🦋 ONGEZA AINA' , callback_data = f'adain {i}')]
                ab3.append(ab2)
            elif i != 10:
                ab1=ab["aina"].split('#@#')[i]
                ab2=[InlineKeyboardButton(text = f'🦋 {ab1}' , callback_data = f'ada2in {i}')]
                ab3.append(ab2)
    ab2=[InlineKeyboardButton(text = f'🦋 RUDI NYUMA' , callback_data = f'zkb')]
    ab3.append(ab2)
    return InlineKeyboardMarkup(ab3)
