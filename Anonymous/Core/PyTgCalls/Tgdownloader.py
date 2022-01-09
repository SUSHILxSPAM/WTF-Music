import asyncio
import time
from datetime import datetime, timedelta

from pyrogram.errors.exceptions import FloodWait

from Anonymous import MUSIC_BOT_NAME, app, db_mem
from Anonymous.Utilities.formatters import bytes
from Anonymous.Utilities.ping import get_readable_time


async def telegram_download(message, mystic):
    ### ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ ʙʏ ᴀɴᴏɴʏᴍᴏᴜs ᴍᴜsɪᴄ ʙᴏᴛ​
    left_time = {}
    speed_counter = {}

    async def progress(current, total):
        if current == total:
            return
        current_time = time.time()
        start_time = speed_counter.get(message.message_id)
        check_time = current_time - start_time
        if datetime.now() > left_time.get(message.message_id):
            percentage = current * 100 / total
            percentage = round(percentage, 2)
            speed = current / check_time
            eta = get_readable_time(int((total - current) / speed))
            if not eta:
                eta = "0 sec"
            total_size = bytes(total)
            completed_size = bytes(current)
            speed = bytes(speed)
            text = f"""
**{MUSIC_BOT_NAME} ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ**

**ᴛᴏᴛᴀʟ ꜰɪʟᴇ sɪᴢᴇ:** {total_size}
**ᴄᴏᴍᴘʟᴇᴛᴇᴅ:** {completed_size}
**ᴘᴇʀᴄᴇɴᴛᴀɢᴇ:** {percentage}%

**sᴘᴇᴇᴅ:** {speed}/s
**ᴇᴛᴀ:** {eta}"""
            try:
                await mystic.edit(text)
            except FloodWait as e:
                await asyncio.sleep(e.x)
            left_time[message.message_id] = datetime.now() + timedelta(
                seconds=5
            )

    speed_counter[message.message_id] = time.time()
    left_time[message.message_id] = datetime.now()
    X = await app.download_media(message.reply_to_message, progress=progress)
    return X