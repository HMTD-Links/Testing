from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters, enums
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)
from pyrogram.types import ReplyKeyboardMarkup
OWNER_ID = Var.OWNER_ID
                      
@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User\n\n᚛›Name :- <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot>File to Link Star Bots</a></b>", parse_mode=ParseMode.HTML
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        await m.reply_photo(
            photo="https://graph.org/file/9853637eaaf2654ccd503.jpg",
            caption="""**Hello 👋🏻 {m.from_user.mention},\n
I'm Star Bots Tamil's Official File to Link Bot (Link Generator Bot). Maintained By :- <a href='https://t.me/Star_Bots_Tamil'>Star Bots Tamil</a>.\n
Click on /help to Get More Information.\n
Warning 🚸\n
🔞 Porn Contents Leads to Permanent Ban You. Check "About 😁"**""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil"), InlineKeyboardButton("👥 Support Group", url="https://t.me/Star_Bots_Tamil_Support")],
                    [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"), InlineKeyboardButton("🤖 Our Bots", url="https://t.me/Star_Bots_Tamil/37")],
                    [InlineKeyboardButton("👨🏻‍✈️ Devloper", url="https://t.me/TG_Karthik")]
                ]
            ),
            
        )
    else:

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.id)

        msg_text = "**ᴛᴏᴜʀ ʟɪɴᴋ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ...⚡\n\n📧 ғɪʟᴇ ɴᴀᴍᴇ :-\n{}\n {}\n\n💌 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :- {}\n\n♻️ ᴛʜɪs ʟɪɴᴋ ɪs ᴘᴇʀᴍᴀɴᴇɴᴛ ᴀɴᴅ ᴡᴏɴ'ᴛ ɢᴇᴛ ᴇxᴘɪʀᴇᴅ ♻️\n\n<b>❖ YouTube.com/@itzjeol</b>**"
        await m.reply_text(            
            text=msg_text.format(file_name, file_size, stream_link),
            
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡ ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ ⚡", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User\n\n᚛›Name :- <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot>File to Link Star Bots</a></b>", parse_mode=ParseMode.HTML
        )
              
    await message.reply_photo(
            photo="https://graph.org/file/9853637eaaf2654ccd503.jpg",
            caption="""**➠ Send Me Any Type of Documents From Telegram.
➠ I will Provide Permanent Direct Download Link, Watch / Stream Link & Shortened Link !
➠ Add me in Your Channel For Direct Download Link Button
➠ This Permanent Link with Fastest Download Speed.
➠ You Can Short Generated Link.\n
Available Commands\n
● /start - Check if 😊 I'm Alive
● /help - How to Use❓
● /about - to Know About Me 😌
● /short - Use This Command with Bot Generated Link 🔗 to Get Shorted Links 🔗
Example :- <code>/short https://t.me/Star_Bots_Tamil</code>\n
Warning ⚠️\n
🔞 Porn Contents Leads to Permanent Ban You.**""", 
  
        
        reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil"), InlineKeyboardButton("👥 Support Group", url="https://t.me/Star_Bots_Tamil_Support")],
                    [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"), InlineKeyboardButton("🤖 Our Bots", url="https://t.me/Star_Bots_Tamil/37")],
                    [InlineKeyboardButton("👨🏻‍✈️ Devloper", url="https://t.me/TG_Karthik")]
                ]
            ),
            
        )

@StreamBot.on_message(filters.command('about') & filters.private)
async def about_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User\n\n᚛›Name :- <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot>File to Link Star Bots</a></b>", parse_mode=ParseMode.HTML
        )
    await message.reply_photo(
            photo="https://graph.org/file/9853637eaaf2654ccd503.jpg",
            caption="""<b>🤖 My Name :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a>\n
🧑🏻‍💻 Developer :- <a href='tg://user?id={OWNER_ID}'><b>Karthik</b></a>\n
📝 Language :- Python3\n
📚 Framework :- Pyrogram\n
📡 Hosted on :- VPS\n
💾 Database :- <a href=https://www.mongodb.com/>Mongo DB</a>\n
🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>\n
🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b>""",
  
        
        reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🤖 Bot Channel", url="https://t.me/Star_Bots_Tamil"), InlineKeyboardButton("👥 Support Group", url="https://t.me/Star_Bots_Tamil_Support")],
                    [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"), InlineKeyboardButton("🤖 Our Bots", url="https://t.me/Star_Bots_Tamil/37")],
                    [InlineKeyboardButton("👨🏻‍✈️ Devloper", url="https://t.me/TG_Karthik")]
                ]
            ),
            
        )
