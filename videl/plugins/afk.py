# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl AFK Status Plugin

import time
from pyrogram import filters, types
from videl import app, db
from videl.helpers._utilities import format_eta


@app.on_message(filters.command(["afk", "brb"]) & ~app.bl_users)
async def afk_handler(_, message: types.Message):
    user_id = message.from_user.id
    reason = message.text.split(None, 1)[1] if len(message.command) > 1 else "Away from keyboard"

    await db.set_afk(user_id, reason)
    await message.reply_text(f"😴 {message.from_user.mention} <b>is now AFK!</b>\n<b>Reason:</b> <i>{reason}</i>", quote=True)


@app.on_message(filters.group & ~filters.me, group=15)
async def afk_listener(_, message: types.Message):
    if not message.from_user:
        return

    # If sender was AFK, remove AFK
    sender_afk = await db.get_afk(message.from_user.id)
    if sender_afk:
        elapsed = int(time.time() - sender_afk["time"])
        await db.clean_afk(message.from_user.id)
        try:
            await message.reply_text(f"👋 Welcome back {message.from_user.mention}! You were AFK for <code>{format_eta(elapsed)}</code>.")
        except Exception:
            pass

    # If message replies to or mentions an AFK user
    if message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
        target_afk = await db.get_afk(target_id)
        if target_afk and target_id != message.from_user.id:
            elapsed = int(time.time() - target_afk["time"])
            await message.reply_text(
                f"😴 {message.reply_to_message.from_user.mention} <b>is currently AFK!</b>\n"
                f"• <b>Reason:</b> <i>{target_afk['reason']}</i>\n"
                f"• <b>Since:</b> <code>{format_eta(elapsed)} ago</code>",
                quote=True,
            )
