# --------------------------------------------------------------------------------
#  Videl © 2026 | Developed by Beasgohan-code
#  Fork & improve freely under MIT. Keep credits.
# --------------------------------------------------------------------------------

import asyncio
import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from videl import bot, LOGGER
from videl.utils.db import add_broadcast_chat, add_served_chat, add_served_user

# Anti-spam: one /start reply per chat every few seconds
_last_start: dict[int, float] = {}
_START_COOLDOWN = 4.0


def _btn(text: str, **kwargs) -> InlineKeyboardButton:
    kwargs.pop("style", None)
    return InlineKeyboardButton(text, **kwargs)


def _start_keyboard() -> InlineKeyboardMarkup | None:
    rows = []
    try:
        link = getattr(config, "BOT_LINK", None) or "https://t.me/"
        rows.append([_btn("➕ Add me to Group", url=f"{link}?startgroup=true")])
    except Exception:
        pass

    row2 = []
    try:
        if getattr(config, "SUPPORT_GROUP", None):
            row2.append(_btn("💬 Support", url=config.SUPPORT_GROUP))
        if getattr(config, "UPDATES_CHANNEL", None):
            row2.append(_btn("📢 Updates", url=config.UPDATES_CHANNEL))
        if row2:
            rows.append(row2)
    except Exception:
        pass

    rows.append([_btn("📖 Help & Commands", callback_data="show_help")])

    row4 = []
    try:
        oid = getattr(config, "OWNER_ID", None)
        if oid:
            row4.append(_btn("👑 Owner", url=f"tg://user?id={oid}"))
        row4.append(_btn("📦 Source", url="https://github.com/Beasgohan-code/Videl"))
        if row4:
            rows.append(row4)
    except Exception:
        pass

    return InlineKeyboardMarkup(rows) if rows else None


def _plain_private(uid: int, name: str) -> str:
    bot_name = getattr(config, "BOT_NAME", "Videl")
    return (
        f"⚡ <b>{bot_name}</b>\n"
        f"Hey <a href='tg://user?id={uid}'><b>{name}</b></a> 👋\n\n"
        f"Telegram <b>Voice Chat</b> music bot.\n\n"
        f"<b>✨ Features</b>\n"
        f"• 🎵 Audio & video in VC\n"
        f"• 🔁 AutoPlay · playlists\n"
        f"• 🎚️ Speed & bass\n"
        f"• 🛡️ Admin tools · 📝 Lyrics\n\n"
        f"<b>🚀 Quick start</b>\n"
        f"1. Add me to your group\n"
        f"2. Give manage video chat rights\n"
        f"3. <code>/play song name</code>\n\n"
        f"Made with ❤️ by <b>Beasgohan</b>"
    )


def _plain_group(uid: int, name: str, title: str) -> str:
    bot_name = getattr(config, "BOT_NAME", "Videl")
    return (
        f"⚡ <b>{bot_name}</b>\n"
        f"Hey <a href='tg://user?id={uid}'><b>{name}</b></a> 👋\n"
        f"Thanks for adding me to <b>{title}</b>.\n\n"
        f"Promote me (manage video chats) then:\n"
        f"<code>/play song name</code> 🎵"
    )


def _start_photo() -> str | None:
    photos = getattr(config, "START_PHOTOS", None) or []
    if not photos:
        return "https://iili.io/n5ClDil.jpg"
    return photos[0]


async def _safe_reply(
    message: Message,
    text: str,
    kb: InlineKeyboardMarkup | None = None,
) -> Message | None:
    """Send exactly one reply (photo+caption or text). Never double-send."""
    chat_id = message.chat.id
    photo = _start_photo()

    if photo:
        try:
            return await message.reply_photo(
                photo=photo,
                caption=text,
                reply_markup=kb,
                quote=True,
            )
        except FloodWait as fw:
            await asyncio.sleep(fw.value + 1)
            try:
                return await message.reply_photo(
                    photo=photo,
                    caption=text,
                    reply_markup=kb,
                    quote=True,
                )
            except Exception as e:
                LOGGER.warning(f"start photo retry failed: {e}")
        except Exception as e:
            LOGGER.warning(f"start photo failed: {e}")

    try:
        return await message.reply_text(
            text,
            reply_markup=kb,
            quote=True,
            disable_web_page_preview=True,
        )
    except FloodWait as fw:
        await asyncio.sleep(fw.value + 1)
        try:
            return await message.reply_text(
                text,
                reply_markup=kb,
                quote=True,
                disable_web_page_preview=True,
            )
        except Exception as e:
            LOGGER.error(f"start text retry failed: {e}")
    except Exception as e:
        LOGGER.error(f"start text failed: {e}")
        try:
            return await bot.send_message(
                chat_id, text, disable_web_page_preview=True
            )
        except Exception as e2:
            LOGGER.error(f"start bare failed: {e2}")
    return None


# Single command name — Pyrogram already matches /start@BotUsername
@bot.on_message(filters.command("start") & ~filters.forwarded, group=0)
async def start_handler(_, message: Message) -> None:
    chat_id = message.chat.id if message.chat else 0
    now = time.time()

    # Drop rapid duplicate /start (double-click, dual handler, etc.)
    last = _last_start.get(chat_id, 0)
    if now - last < _START_COOLDOWN:
        return
    _last_start[chat_id] = now

    # Keep dict small
    if len(_last_start) > 500:
        cutoff = now - 60
        for k in [k for k, t in _last_start.items() if t < cutoff]:
            _last_start.pop(k, None)

    try:
        uid = message.from_user.id if message.from_user else 0
        name = (message.from_user.first_name if message.from_user else "User") or "User"
        name = name.replace("<", "").replace(">", "")
        chat_type = message.chat.type

        try:
            if uid:
                add_served_user(uid)
            add_served_chat(chat_id)
        except Exception:
            pass

        try:
            kb = _start_keyboard()
        except Exception as e:
            LOGGER.warning(f"start keyboard: {e}")
            kb = None

        if chat_type == ChatType.PRIVATE:
            text = _plain_private(uid, name)
            await _safe_reply(message, text, kb)
            try:
                add_broadcast_chat(chat_id, "private")
            except Exception:
                pass
            return

        # Groups / super groups — one message only
        title = (message.chat.title or "this chat").replace("<", "").replace(">", "")
        text = _plain_group(uid, name, title)
        await _safe_reply(message, text, kb)

        try:
            add_broadcast_chat(chat_id, "group")
        except Exception:
            pass

    except Exception as e:
        LOGGER.error(f"/start handler crash: {e}")
        # Do not send a second error message if we already replied
        if now - _last_start.get(chat_id, 0) < 1:
            return
        try:
            await message.reply_text("⚡ Bot is online. Use /play in a group.")
        except Exception:
            pass


@bot.on_message(filters.command("help") & ~filters.forwarded, group=0)
async def help_handler(_, message: Message) -> None:
    try:
        kb = InlineKeyboardMarkup([
            [
                _btn("🎵 Play", callback_data="help_play"),
                _btn("⚙️ Admin", callback_data="help_admin"),
            ],
            [
                _btn("🛠️ Tools", callback_data="help_tools"),
                _btn("ℹ️ Extra", callback_data="help_extra"),
            ],
            [_btn("🏠 Home", callback_data="start_home")],
        ])
        text = (
            "📖 <b>Help menu</b>\n\n"
            "• <code>/play song</code>\n"
            "• <code>/vplay song</code>\n"
            "• <code>/cplay song</code>\n"
            "• <code>/pause</code> · <code>/skip</code> · <code>/stop</code>\n"
            "• <code>/queue</code> · <code>/lyrics</code>\n"
            "• <code>/ping</code>"
        )
        await message.reply_text(
            text,
            reply_markup=kb,
            quote=True,
            disable_web_page_preview=True,
        )
    except Exception as e:
        LOGGER.error(f"/help failed: {e}")
        try:
            await message.reply_text(
                "📖 /play /vplay /pause /skip /stop /queue /lyrics /ping"
            )
        except Exception:
            pass
