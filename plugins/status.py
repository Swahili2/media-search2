import datetime
from info import CHANNELS
from plugins.database import db
from utils import is_user_exist
async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id if cmd.from_user else None
    if chat_id:
        if not await is_user_exist(chat_id):
            await add_user(chat_id,cmd.chat.id)
            await bot.send_message(
                chat_id= CHANNELS,
                text=f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started!!"
            )
