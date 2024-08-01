import os
from telegraph import upload_file
import pyrogram
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Sample configuration. Replace these with actual values.
class Config:
    APP_ID = '2170492'
    API_HASH = '82b683da442942d5c177ec520318a32f'
    TG_BOT_TOKEN = '7304879730:AAHWnILVrNQjeD7QuLMd3UOuC5xf72mzd5I'

# Initialize Pyrogram Client
Tgraph = Client(
    "Telegra.ph Uploader",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN,
)

# Ensure DOWNLOADS directory exists
if not os.path.exists('./DOWNLOADS'):
    os.makedirs('./DOWNLOADS')

async def upload_media(client, message, file_type, file_extension, size_limit=5242880):
    if message.document and message.document.file_size > size_limit:
        await message.reply_text("Size should be less than 5 MB.")
        return

    msg = await message.reply_text("`Trying to download`")
    user_id = str(message.chat.id)
    file_path = f"./DOWNLOADS/{user_id}{file_extension}"
    
    # Download media
    file_path = await client.download_media(message=message, file_name=file_path)
    await msg.edit_text("`Trying to upload.....`")

    try:
        tlink = upload_file(file_path)
        await msg.edit_text(f"https://telegra.ph{tlink[0]}")
    except Exception as e:
        await msg.edit_text("`Something went wrong`")
        print(f"Error: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@Tgraph.on_message(filters.photo)
async def upload_photo(client, message):
    await upload_media(client, message, "photo", ".jpg")

@Tgraph.on_message(filters.animation)
async def upload_gif(client, message):
    await upload_media(client, message, "gif", ".mp4")

@Tgraph.on_message(filters.video)
async def upload_video(client, message):
    await upload_media(client, message, "video", ".mp4")

@Tgraph.on_message(filters.command(["start"]))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ],
        [
            InlineKeyboardButton('Our Channel', url='http://telegram.me/indusbots'),
            InlineKeyboardButton('Source Code', url='https://github.com/benchamxd/Telegraph-Uploader')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        text="""<b>Hey there,

I am a telegraph Uploader Bot that can upload photos, videos, and gifs to Telegra.ph.

Simply send me a photo, video, or gif to upload.

Made with love by @indusBots</b>""",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=message.message_id
    )

@Tgraph.on_message(filters.command(["help"]))
async def help(client, message):
    buttons = [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Close', callback_data='close')
        ],
        [
            InlineKeyboardButton('Our Channel', url='http://telegram.me/indusbots')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        text="""<b>Help Information:</b>
        
Just send me a video, gif, or photo up to 5 MB.

I'll upload it to Telegra.ph and give you the direct link.""",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=message.message_id
    )

@Tgraph.on_callback_query()
async def button(client, update):
    cb_data = update.data
    if "help" in cb_data:
        await update.message.delete()
        await help(client, update.message)
    elif "close" in cb_data:
        await update.message.delete()
    elif "home" in cb_data:
        await update.message.delete()
        await start(client, update.message)

Tgraph.run()
