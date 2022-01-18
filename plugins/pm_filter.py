@Client.on_message(filters.text & filters.group & filters.incoming)
async def group(client, message):
    await handle_user_status(client,message)
