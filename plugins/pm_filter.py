from program import Client
from info import filters
from status import handle_user_status
@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    await handle_user_status(client,message)
