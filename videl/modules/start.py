# --------------------------------------------------------------------------------
#  Videl © 2026 | Developed by Beasgohan-code
#  Fork & improve freely under MIT. Keep credits.
# --------------------------------------------------------------------------------

import asyncio
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from videl import bot, LOGGER
from videl.modules.block import user_allowed
from videl.utils.db import add_broadcast_chat, add_served_chat, add_served_user


def _btn(text: str, **kwargs) -> InlineKeyboardButton:
    """Build a button without ButtonStyle (avoids crashes on older clients)."""
    # Drop unsupported kwargs like style=
    kwargs.pop("style", None)
    return InlineKeyboardButton(text, **kwargs)


def _start_keyboard() -> InlineKeyboardMarkup:
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
        rows.append(row4)
    except Exception:
        pass

    return InlineKeyboardMarkup(rows) if rows else None


def _plain_private(uid: int, name: str) -> str:
    bot_name = getattr(config, "BOT_NAME", "Videl")
    return (
        f"⚡ <b>{bot_name}</b>\n\n"
        f"Hey <a href='tg://user?id={uid}'><b>{name}</b></a> 👋\n\n"
        f"Welcome to <b>{bot_name}</b> — a Telegram VC music bot.\n\n"
        f"<b>✨ Features</b>\n"
        f"• 🎵 Audio & video in VC\n"
        f"• 🔁 AutoPlay · playlists\n"
        f"• 🎚️ Speed & bass effects\n"
        f"• 🛡️ Group admin tools\n"
        f"• 📝 Lyrics · 📢 Channel play\n\n"
        f"<b>🚀 Quick start</b>\n"
        f"1. Add me to your group\n"
        f"2. Give manage video chat rights\n"
        f"3. Send <code>/play song name</code>\n\n"
        f"Made with ❤️ by <b>Beasgohan</b>"
    )


def _plain_group(uid: int, name: str, title: str) -> str:
    bot_name = getattr(config, "BOT_NAME", "Videl")
    return (
        f"⚡ <b>{bot_name}</b>\n\n"
        f"Hey <a href='tg://user?id={uid}'><b>{name}</b></a> 👋\n"
        f"Thanks for adding me to <b>{title}</b>.\n\n"
        f"Send <code>/play song name</code> to start 🎵"
    )


async def _safe_reply(chat_id: int, text: str, kb=None) -> Message | None:
    """Always try to show something — photo → text → bare text."""
    photos = getattr(config, "START_PHOTOS", None) or []
    photo = random.choice(photos) if photos else None

    if photo:
        try:
            return await bot.send_photo(
                chat_id,
                photo=photo,
                caption=text,
                reply_markup=kb,
            )
        except FloodWait as fw:
            await asyncio.sleep(fw.value + 1)
            try:
                return await bot.send_photo(
                    chat_id, photo=photo, caption=text, reply_markup=kb
                )
            except Exception as e:
                LOGGER.warning(f"start photo retry failed: {e}")
        except Exception as e:
            LOGGER.warning(f"start photo failed: {e}")

    try:
        return await bot.send_message(
            chat_id,
            text,
            reply_markup=kb,
            disable_web_page_preview=True,
        )
    except FloodWait as fw:
        await asyncio.sleep(fw.value + 1)
        try:
            return await bot.send_message(
                chat_id, text, reply_markup=kb, disable_web_page_preview=True
            )
        except Exception as e:
            LOGGER.error(f"start text retry failed: {e}")
    except Exception as e:
        LOGGER.error(f"start text failed: {e}")
        # Last resort — no keyboard
        try:
            return await bot.send_message(chat_id, text, disable_web_page_preview=True)
        except Exception as e2:
            LOGGER.error(f"start bare failed: {e2}")
    return None


@bot.on_message(filters.command(["start", "start@"]))
async def start_handler(_, message: Message) -> None:
    """
    /start — no heavy filters, always replies.
    Blocked users are still allowed to see start (harmless).
    """
    try:
        uid = message.from_user.id if message.from_user else 0
        name = (message.from_user.first_name if message.from_user else "User") or "User"
        # strip HTML-ish chars
        name = name.replace("<", "").replace(">", "")
        chat_id = message.chat.id
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
            await _safe_reply(chat_id, text, kb)
            try:
                add_broadcast_chat(chat_id, "private")
            except Exception:
                pass
            return

        title = (message.chat.title or "this chat").replace("<", "").replace(">", "")
        text = _plain_group(uid, name, title)
        await _safe_reply(chat_id, text, kb)

        try:
            await bot.send_message(
                chat_id,
                "✅ <b>Almost ready</b>\n\n"
                "Make me <b>admin</b> with:\n"
                "• Delete messages\n"
                "• Manage video chats\n"
                "• Invite users",
            )
        except Exception:
            pass

        try:
            add_broadcast_chat(chat_id, "group")
        except Exception:
            pass

    except Exception as e:
        LOGGER.error(f"/start handler crash: {e}")
        try:
            await message.reply_text(
                f"⚡ Bot is online.\nUse /play song name in a group.\n\n<code>{e}</code>"
            )
        except Exception:
            try:
                await bot.send_message(
                    message.chat.id,
                    "⚡ Bot is online. Use /play in a group.",
                )
            except Exception:
                pass


@bot.on_message(filters.command(["help", "help@"]))
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
            "Tap a category below, or try:\n"
            "• <code>/play song</code>\n"
            "• <code>/vplay song</code>\n"
            "• <code>/cplay song</code>\n"
            "• <code>/pause</code> · <code>/skip</code> · <code>/stop</code>\n"
            "• <code>/queue</code> · <code>/lyrics</code>\n"
            "• <code>/ping</code>"
        )
        await bot.send_message(
            message.chat.id,
            text,
            reply_markup=kb,
            disable_web_page_preview=True,
        )
    except Exception as e:
        LOGGER.error(f"/help failed: {e}")
        try:
            await message.reply_text(
                "📖 Commands:\n"
                "/play /vplay /cplay /pause /skip /stop /queue /lyrics /ping"
            )
        except Exception:
            pass
