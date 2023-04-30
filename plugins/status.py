from info import CHANNELS ,OWNER_ID
from datetime import datetime 
import time
from plugins.database import db
from utils import is_user_exist,add_user,User,get_file_details
async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id if cmd.from_user else None
    if chat_id:
        ab=await is_user_exist(cmd.chat.id)
        if not (await is_user_exist(chat_id)):
            if not ab:
                return
            await add_user(chat_id,cmd.chat.id,'user')
            await bot.send_message(
                chat_id= CHANNELS,
                text=f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started on {cmd.chat.title}!!"
            )
            
        if ab:
            await User.collection.update_one({'_id':chat_id},{'$set':{'group_id':cmd.chat.id}})
        else:
            return
        for uza in ab:
            status = uza.group_id
       
        ban_status = await db.get_ban_status(status)
        if not ban_status["is_banned"]:
            return
    else:
        return
async def handle_admin_status(bot, cmd):
        all_user =await db.get_all_users()
        async for user in all_user:
            ban_status = await db.get_ban_status(user['id'])
            if ban_status["is_banned"]:
                if ban_status["ban_duration"] < (
                        datetime.now() - datetime.fromisoformat(ban_status["banned_on"])
                ).days:
                    await bot.send_message(chat_id=int(user['id']),text=f"Samahan admin kifurushi ulicho lipia kumtumia swahili robot kimeisha tafadhali lipia ili wateja wako waendelee kupata huduma zetu")
                    await db.remove_ban(user['id'])
        all_users =await db.get_all_acc()
        async for user in all_users:
            
            if user["ban_status"]["ban_duration"] < (datetime.now() - datetime.fromisoformat(user["ban_status"]["banned_on"])).days:
                if user['file_id'].startswith('g_'):
                    abc=await db.get_db_status(user['db_name'])
                    abc=f"{abc[user['file_id']].split('#@')[0]} kimeisha"
                else:
                    for file in await get_file_details(user['file_id']):
                        abc=f"{file.text.split('.dd#.')[0]} mda wake wa kuipakua umeisha"
                await bot.send_message(chat_id=int(user['user_id']),text=f"{abc} tafadhali jiunge kuendelea kupata huduma zetu kwa bei nafuu")
                await db.delete_acc(user['id'])
