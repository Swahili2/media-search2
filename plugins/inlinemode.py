from pyrogram import Client
import re
import ast
from plugins.database import db
from pyrogram.types import (
    InlineQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedDocument
)
from utils import is_user_exist,get_search_results,Media,is_group_exist
from info import filters
BOT = {}
@Client.on_inline_query(filters.inline)
async def give_filter(client: Client, query):
    userdetails= await is_user_exist(query.from_user.id)
    status= await db.is_admin_exist(query.from_user.id)
    a='no'
    nyva=BOT.get("username")
    if not nyva:
        botusername=await client.get_me()
        nyva=botusername.username
        BOT["username"]=nyva
    if not status:
        a='yes'
    await client.send_message( chat_id=query.from_user.id,text=f'{userdetails}')
    if not userdetails:
        if a =='no':
            result=[]
            title = f"🎁🎁 Mpendwa :{query.from_user.first_name} 🎁🎁"
            text1= f"!!HAUPO KWENYE DATABASE YANGU!!\nMimi naitwa Muhsin alimaarufu Swahili Robot, Username @bandolako2bot\nMimi ni  Robot ninayerahisisha uuzaji wa movie au series za jumla na rejareja bila ya usumbufu wa admini kila SAA kutuma muv na series kazi yake kubwa ni  kuthibitisha malipo.\nKujua nnavyofanya kazi ,jinsi ya kujiunga,maelekezo ya kutumia huduma hizi jiunge na kikundi chetu @swahilichats au wasiliana @hrm45 atakupa maelezo zaidi Nb Kwa wageni wanaojiunga na kutafta jinsi ya kupata movie na series tafadhali join @swahilichats kupata msaada zaidi\n\nBonyeza 👨‍👧‍👧 join group kujiunga"
            result.append(InlineQueryResultArticle(
                    title=title,
                    input_message_content=InputTextMessageContent(message_text = text1, disable_web_page_preview = True),
                    description=f'!!HAUPO KWENYE DATABASE YANGU!!\nKitu chochote utakacho niuliza ntashindwa kukujibu,Ili kupata movie,series,miziki n.k gusa hapa kupata maelekezo ya kujiunga',
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('👨‍👧‍👧 join group', url=file.inv_link)]])
                ))
            await query.answer(
                results = result,
                is_personal = True,
                switch_pm_text = f'Mpendwa {query.from_user.first_name} haupo kwenye Database',
                switch_pm_parameter = 'start'
            )
            return
    for user in userdetails:
        group_details = await is_user_exist(user.group_id)
        grp_id=user.group_id
        for id2 in group_details:
            group_id = id2.group_id

            
    text = query.query
    ban = await db.get_ban_status(group_id) 
    offset = int(query.offset or 0)
    documents, next_offset = await get_search_results(text,
                                              group_id = group_id,
                                              max_results=10,
                                              offset=offset)
    results = []
    for document in documents:
        id3 = document['id']
        reply_text = document['reply']
        button = document['btn']
        alert = document['alert']
        file_status = document['status']
        fileid = document['file']
        keyword = document['text'].split('.dd#.',1)[0]
        msg_type = document['type']
        descp = document['descp'].split('.dd#.')[1]
        acs = document['descp'].split('.dd#.')[0]
        if button == "[]":
            button = None
        
        if reply_text:
            reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
        if acs == 'x':  
            if fileid == 'None':
                try:
                    result = InlineQueryResultArticle(
                        title=keyword.upper(),
                        input_message_content=InputTextMessageContent(message_text = reply_text, disable_web_page_preview = True,
                            parse_mode = 'html'),
                        description=descp,
                        reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
                    )
                except:
                    continue
            elif msg_type == 'Photo' and ban['status'] == 'vip' and file_status == 'vip':
                try:
                    result = InlineQueryResultPhoto(
                        photo_url = fileid,
                        title = keyword.upper(),
                        description = descp,
                        parse_mode = 'html',
                        caption = reply_text,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{id3}")]])
                    )
                except:
                    continue
            elif msg_type == 'Photo':
                try:
                    result = InlineQueryResultPhoto(
                        photo_url = fileid,
                        title = keyword.upper(),
                        description = descp,
                        parse_mode = 'html',
                        caption = reply_text or '',
                        reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
                    )
                except:
                    continue
            elif fileid and ban['status'] == 'vip' and file_status == 'vip':
                try:
                    result = InlineQueryResultCachedDocument(
                        title = keyword.upper(),
                        file_id = fileid,
                        caption = reply_text or "",
                        parse_mode = 'html',
                        description = descp,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('📤 Download', url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{id3}")]])
                    )
                except:
                    continue
            elif fileid:
                try:
                    result = InlineQueryResultCachedDocument(
                        title = keyword.upper(),
                        file_id = fileid,
                        caption = reply_text or "",
                        parse_mode = 'html',
                        description = descp,
                        reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
                    )
                except:
                    continue
            else:
                continue

            results.append(result)
        
    if len(results) != 0:
        switch_pm_text = f"Total {len(results)} Matches"
    else:
        switch_pm_text = "No matches"
    if not ban['is_banned']and len(results) != 0 and group_id !=query.from_user.id:
        result=[]
        ttl=await client.get_users(group_id)
        ttl2 = await client.get_chat(grp_id)
       
        title = f"🎁🎁 Mpendwa {query.from_user.first_name} 🎁🎁"
        st = await client.get_chat_member(grp_id, "me")
        if (st.status == "administrator"):
            text1= f"Kifurush cha group kimeisha\n Yaan ada ya admin anayotakiwa kulipia ili kuendelea kumtumia Swahili robot kwenye group \n 👨‍👨‍👧‍👧 Group name:**{ttl2.title}**\n\n🙍🙍‍♀ Admin name:[{ttl.first_name.upper()}](tg://user?id={group_id})Bonyeza MTAARIFU ADMIN kisha mkumbushe alipie kifurush ili muweze kuendelee kumtumia robot"
        else:
            text1= f"Kifurush cha group kimeisha\n Yaan ada ya admin anayotakiwa kulipia ili kuendelea kumtumia Swahili robot kwenye group \n 👨‍👨‍👧‍👧 Group name:**{ttl2.title}**\n\n🙍🙍‍♀ Admin name:[{ttl.first_name.upper()}](tg://user?id={group_id})Bonyeza MTAARIFU ADMIN kisha mkumbushe alipie kifurush kisha aniadd kama admin kwenye group hili ili muweze kuendelee kumtumia robot"
        result.append(InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(message_text = text1, disable_web_page_preview = True),
                description=f'total members :\nGusa hapa kujoin g kupata movie series miziki nakadhalika kupitia Swahili robot',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('👨‍👧‍👧 MTAARIFU ADMIN', url=f'(tg://user?id={group_id})')]])
            ))
        await query.answer(
            results = result,
            is_personal = True,
            switch_pm_text = 'Admin wako hajalipia kifurushi',
            switch_pm_parameter = 'start'
        )
        return
    await query.answer(
        results = results,
        is_personal = True,
        cache_time = 300,
        next_offset =str(next_offset)
    )
        
        
@Client.on_callback_query(filters.regex(r"^(alertmessage):(\d):(.*)"))
async def alert_msg(client: Client, callback):
    regex = r"^(alertmessage):(\d):(.*)"
    matches = re.match(regex, callback.data)
    i = matches.group(2)
    id = matches.group(3)
    filter = {'id': id}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    for alert in filedetails:
        alerts = alert.alert
    if alerts:
        alerts = ast.literal_eval(alerts)
        alert = alerts[int(i)]
        alert = alert.replace("\\n", "\n").replace("\\t", "\t")
        try:
            await callback.answer(alert,show_alert=True)
        except:
            pass
