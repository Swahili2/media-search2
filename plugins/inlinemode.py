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
from utils import is_user_exist,get_search_results,Media
from info import filters
@Client.on_inline_query(filters.inline)
async def give_filter(client: Client, query):
    userdetails= await is_user_exist(query.from_user.id)
    if not userdetails:
        all_user =await db.get_all_users()
        result=[]
        async for user in all_user:
            ban_status = await db.get_ban_status(user['id'])
            if ban_status["is_banned"]:
                ttl =await client.get_users(user['id'])
                title =ttl.first_name
                result.append(InlineQueryResultArticle(
                    title=f'Admin {title}',
                    input_message_content=InputTextMessageContent(message_text = f'gshdhjdjdh'),
                    description='Tafadhali nchague mimi ntakuelekeza jinsi ya kupata muv,sizon na miendelezo n.k always nipo active ',
                ))
                
        await query.answer(
            results = result,
            is_personal = True,
            switch_pm_text = f'Samahani {query.from_user.first_name} haupo kwenye Database zetu',
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

        if button == "[]":
            button = None
        
        if reply_text:
            reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
            
        if fileid == 'None':
            try:
                result = InlineQueryResultArticle(
                    title=keyword.upper(),
                    input_message_content=InputTextMessageContent(message_text = reply_text, disable_web_page_preview = True,
                        parse_mode = 'html'),
                    description='Text',
                    reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
                )
            except:
                continue
        elif msg_type == 'Photo':
            try:
                result = InlineQueryResultPhoto(
                    photo_url = fileid,
                    title = keyword.upper(),
                    description = 'Photo',
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
                    description = msg_type,
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
    if not ban['is_banned']and len(results) != 0:
        all_user =await db.get_all_users()
        resultz=[]
        async for user in all_user:
            ban_status = await db.get_ban_status(user['id'])
            if ban_status["is_banned"]:
                ttl =await client.get_users(user['id'])
                
                resultz.append(InlineQueryResultArticle(
                    title=f'Admin {(ttl.first_name).upper()}',
                    input_message_content=InputTextMessageContent(message_text = 'hii ni kwa sababu admin hajalipia kifurush'),
                    description='Tafadhal nchague Mimi nipo active mda wote'
                ))
        await query.answer(
            results = resultz,
            is_personal = True,
            switch_pm_text = 'Admin wako hajalipia kifurushi tafadhali  chagua active admin kwenye list',
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
