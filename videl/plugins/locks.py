# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Group Locks & Permissions Enforcement Plugin

import re
from pyrogram import filters, types
from videl import app, db
from videl.helpers._admins import admin_check, is_admin

LOCK_TYPES = [
    "stickers",
    "media",
    "links",
    "voice",
    "forward",
    "bots",
    "polls",
]


@app.on_message(filters.command(["locks", "locklist"]) & filters.group & ~app.bl_users)
async def list_locks(_, message: types.Message):
    active_locks = await db.get_locks(message.chat.id)
    text = f"🔒 <b><u>Active Chat Locks in {message.chat.title}</u></b>\n\n"

    for lock in LOCK_TYPES:
        status = "🔒 Locked" if lock in active_locks else "🔓 Unlocked"
        text += f"• <b>{lock.capitalize()}:</b> <code>{status}</code>\n"

    text += "\n<i>Toggle with: <code>/lock [type]</code> or <code>/unlock [type]</code></i>"
    await message.reply_text(text, quote=True)


@app.on_message(filters.command(["lock", "unlock"]) & filters.group & ~app.bl_users)
@admin_check
async def toggle_lock(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"<b>Usage:</b> <code>/{message.command[0]} [lock type]</code>\n\n"
            f"<b>Supported Types:</b> <code>{', '.join(LOCK_TYPES)}</code>",
            quote=True,
        )

    lock_type = message.command[1].lower()
    enable = message.command[0].lower() == "lock"

    if lock_type == "all":
        for l in LOCK_TYPES:
            await db.set_lock(message.chat.id, l, enable)
        return await message.reply_text(f"🔒 <b>{'Locked' if enable else 'Unlocked'} all permissions!</b>", quote=True)

    if lock_type not in LOCK_TYPES:
        return await message.reply_text(f"❌ Invalid lock type! Supported: <code>{', '.join(LOCK_TYPES)}</code>", quote=True)

    await db.set_lock(message.chat.id, lock_type, enable)
    await message.reply_text(f"🔒 <b>{lock_type.capitalize()}</b> is now <b>{'Locked' if enable else 'Unlocked'}</b>.", quote=True)


@app.on_message(filters.group & ~filters.me, group=12)
async def lock_enforcer(_, message: types.Message):
    if not message.from_user:
        return

    # Skip admins
    if await is_admin(message.chat.id, message.from_user.id):
        return

    active_locks = await db.get_locks(message.chat.id)
    if not active_locks:
        return

    violates = False

    if "stickers" in active_locks and (message.sticker or message.animation):
        violates = True
    elif "media" in active_locks and (message.photo or message.video or message.audio or message.document or message.voice):
        violates = True
    elif "voice" in active_locks and (message.voice or message.video_note):
        violates = True
    elif "forward" in active_locks and message.forward_date:
        violates = True
    elif "polls" in active_locks and message.poll:
        violates = True
    elif "links" in active_locks:
        text = message.text or message.caption or ""
        if re.search(r"(https?://\S+|t\.me/\S+|telegram\.me/\S+)", text):
            violates = True

    if violates:
        try:
            await message.delete()
        except Exception:
            pass
