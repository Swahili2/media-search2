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
@Client.on_inline_query(filters.inline)
async def give_filter(client: Client, query):
    userdetails= await is_user_exist(query.from_user.id)
    status= await db.is_admin_exist(query.from_user.id)
    a='no'
    if not status:
        a='yes'
    if not userdetails:
        if a =='no':
            all_user =await is_group_exist('group')
            result=[]
            for file in all_user:
                ban_status = await db.get_ban_status(file.group_id)
                if ban_status["is_banned"]:
                    ttl=await client.get_users(file.group_id)
                    title = f"🎁🎁 GROUP :{file.title} 🎁🎁"
                    text1= f"!!HAUPO KWENYE DATABASE!!\n(jiunge kuanza kupata huduma zetu)👨‍👨‍👧‍👧 Group name:**{file.title}**\n\n👨‍👧‍👧 Total_members : **{file.total_m}**\n\n🙍🙍‍♀ Admin name:[{ttl.first_name.upper()}](tg://user?id={file.group_id})\n\nJiunge sasa uweze kupata muv,sizon zilizotafsiriwa na ambazo hazijatafsiriwa,miziki,vichekesho n.k kupitia swahili robot\nUkisha join tuma neno `hi`\n\n°°Kumbuka admin kifurush chake kikiisha hii menyu ya groups utaiona tena ili kupata active groups ambapo swahili robot yupo active\n\nBonyeza 👨‍👧‍👧 join group kujiunga"
                    result.append(InlineQueryResultArticle(
                            title=title,
                            input_message_content=InputTextMessageContent(message_text = text1, disable_web_page_preview = True),
                            description=f'total members : {file.total_m} \nGusa hapa kujoin group kupata movie series miziki nakadhalika kupitia Swahili robot',
                            thumb_url=file.link,
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
        reply_text = document['reply']
        button = document['btn']
        alert = document['alert']
        fileid = document['file']
        keyword = document['text']
        msg_type = document['type']
        descp = document['descp']

        if button == "[]":
            button = None
        
        if reply_text:
            reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
            
        if fileid == 'None':
            try:
                await client.send_message(chat_id=query.from_user.id,text=f'{button}')
                result = InlineQueryResultArticle(
                    title=keyword.upper(),
                    input_message_content=InputTextMessageContent(message_text = reply_text, disable_web_page_preview = True,
                        parse_mode = 'html'),
                    description=descp,
                    reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
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
        all_user =await is_group_exist('group')
        result=[]
        for file in all_user:
            ban_status = await db.get_ban_status(file.group_id)
            if ban_status["is_banned"]:
                ttl=await client.get_users(file.group_id)
                title = f"🎁🎁 GROUP :{file.title} 🎁🎁"
                text1= f"Join now kuendelea kumtumia Swahili robot.👨‍👨‍👧‍👧 Group name:**{file.title}**\n\n👨‍👧‍👧 Total_members : **{file.total_m}**\n\n🙍🙍‍♀ Admin name:[{ttl.first_name.upper()}](tg://user?id={file.group_id})\n\nJiunge sasa uweze kupata muv,sizon zilizotafsiriwa na ambazo hazijatafsiriwa,miziki,vichekesho n.k kupitia swahili robot\nUkisha join tuma neno `hi`\n\n°°Kumbuka admin kifurush chake kikiisha hii menyu ya groups utaiona tena ili kuapata active groups ambapo swahili robot yupo active\n\nBonyeza 👨‍👧‍👧 join group kujiunga"
                result.append(InlineQueryResultArticle(
                        title=title,
                        input_message_content=InputTextMessageContent(message_text = text1, disable_web_page_preview = True),
                        description=f'total members : {file.total_m} \nGusa hapa kujoin group kupata movie series miziki nakadhalika kupitia Swahili robot',
                        thumb_url=file.link,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('👨‍👧‍👧 join group', url=file.inv_link)]])
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
