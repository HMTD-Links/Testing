import os
import aiohttp
import asyncio
import urllib.parse
import logging
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.handlers import MessageHandler
from pyshorteners import Shortener
from pyrogram import filters, errors, Client, enums
from Adarsh.vars import Var
from urllib.parse import quote_plus
from Adarsh.utils.database import Database
from Adarsh.bot import StreamBot
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import get_name, get_media_file_size, get_hash
from pyrogram.errors import FloodWait, UserNotParticipant
from pyshorteners import Shortener
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


async def get_shortlink(link):
    url = 'https://tnshort.net/api'
    params = {'api': "d03a53149bf186ac74d58ff80d916f7a79ae5745", 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            return data["shortenedUrl"]

def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User\n\n᚛›Name :- <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot>File to Link Star Bots</a></b>", parse_mode=ParseMode.HTML
        )
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        file_name = get_name(log_msg)
        file_hash = get_hash(log_msg)
        watch_link = f"{Var.URL}Watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        file_size = humanbytes(get_media_file_size(m))
        file_caption = m.caption
        shortened_stream_link = await get_shortlink(stream_link)
        shortened_watch_link = await get_shortlink(watch_link)
        
        msg_text ="""<b>Your Link is Generated... ⚡\n\n📁 File Name :- {file_name}\n\n📦 File Size :- {file_size}\n\n🔠 File Captain :- {file_caption}\n\n📥 Fast Download Link :- {}\n\n🖥 Watch Link :- {}\n\n❗ Note :- This Link is Permanent and Won't Gets Expired 🚫\n\n©️ <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b></b>"""

        await log_msg.reply_text(text=f"<b>Request By :- <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>\nID :- <code>{m.from_user.id}</code>\n📥 Download Link :- {stream_link}</b>", disable_web_page_preview=True, parse_mode=ParseMode.HTML, quote=True)
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link, watch_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Fast Download Link", url=stream_link), #Download Link
                                                InlineKeyboardButton('🖥 Watch Link', url=watch_link)]]) #Stream Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"<b>Got FloodWait of {str(e.x)}s from <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n\nUser ID :- <code>{str(m.from_user.id)}</code></b>", disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@StreamBot.on_message(
    filters.channel
    & (
        filters.document
        | filters.video
    ),
    group=4,
)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        file_name = get_media_file_name(broadcast)
        file_hash = get_hash(log_msg)
        stream_link = "https://{}/{}/{}?hash={}".format(Var.FQDN, log_msg.id, file_name, file_hash) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}?hash={}".format(Var.FQDN,
                                    Var.PORT,
                                    log_msg.id,
                                    file_name,
                                    file_hash)
        shortened_link = await get_shortlink(stream_link)

        await log_msg.reply_text(
            text=f"<b>Channel Name :- {broadcast.chat.title}\nChannel ID :- <code>{broadcast.chat.id}</code>\nRequest URL :- https://t.me/{(await bot.get_me()).username}?start=Star_Bots_Tamil_{str(log_msg.id)}</b>",
            quote=True,
            parse_mode=ParseMode.HTML
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📥 Fast Download Link", url=f"https://t.me/{(await bot.get_me()).username}?start=Star_Bots_Tamil_{str(log_msg.id)}")]])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"<b>Got FloodWait of {str(w.x)}s From {broadcast.chat.title}\n\nChannel ID :-</b> <code>{str(broadcast.chat.id)}</code>",
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"<b>#Error_Trackback :-</b> <code>{e}</code>", disable_web_page_preview=True, parse_mode=ParseMode.HTML)
        print(f"Can't Edit Broadcast Message!\nError :- {e}")
