from pyrogram import Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
import asyncio
import os
import time

async def process_file(update, bot, ms, media, new_filename, c_thumb, dl, duration):
    # Generate caption
    caption = f"**{new_filename}**"

    # Handle thumbnail
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    # Notify user to wait
    await ms.edit("__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__")

    # Determine type and send the file
    type = update.data.split("_")[1]
    try:
        if type == "document":
            print("Starting upload...")
            await bot.send_document(
                update.from_user.id,
                document=dl,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__**Please wait...**__\n🌨️ **Upload Started....**", ms, time.time())
            )
            print("Upload completed.")

        elif type == "video":
            await bot.send_video(
                update.from_user.id,
                video=dl,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
            )
        elif type == "audio":
            await bot.send_audio(
                update.from_user.id,
                audio=dl,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
            )
    except Exception as e:
        os.remove(dl)
        if ph_path:
            os.remove(ph_path)
        return await ms.edit(f" Eʀʀᴏʀ {e}")

    # Clean up
    try:
        os.remove(dl)
        if ph_path:
            os.remove(ph_path)
    except Exception as e:
        print(e)

    # Notify the user in a supergroup chat or delete the message
    if update.message.chat.type == enums.ChatType.SUPERGROUP:
        botusername = await bot.get_me()
        await ms.edit(f"Hey {update.from_user.mention},\n\nI Have Send Renamed File To Your Pm", 
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Bᴏᴛ Pᴍ", url=f'https://t.me/{botusername.username}')]]))
    else:
        await ms.delete()

async def send_debug_message(user_id, message):
    async with Client("my_bot") as bot:
        await bot.send_message(user_id, message)

async def progress_for_pyrogram(current, total, message, ms, start_time):
    now = time.time()
    diff = now - start_time
    if round(diff % 10) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        eta = (total - current) / speed
        text = f"Progress: {percentage:.2f}%\nSpeed: {speed:.2f}B/s\nETA: {eta:.2f}s"
        await ms.edit(text)
        
