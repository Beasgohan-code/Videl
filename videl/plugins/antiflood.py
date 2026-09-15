# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Anti-Flood Protection Plugin

import time
from collections import defaultdict
from pyrogram import filters, types
from videl import app, db
from videl.helpers._admins import admin_check, is_admin

user_msg_times = defaultdict(lambda: defaultdict(list))


@app.on_message(filters.command(["antiflood", "setflood", "flood"]) & filters.group & ~app.bl_users)
@admin_check
async def set_flood_cmd(_, message: types.Message):
    if len(message.command) < 2:
        current = await db.get_flood(message.chat.id)
        return await message.reply_text(
            f"🛡 <b>Anti-Flood Status:</b> <code>{f'{current} messages/5s' if current > 0 else 'Disabled'}</code>\n\n"
            "<b>Usage:</b>\n"
            "• <code>/antiflood 5</code> (Set limit to 5 messages/5s)\n"
            "• <code>/antiflood off</code> (Disable anti-flood)",
            quote=True,
        )

    val = message.command[1].lower()
    if val in ("off", "disable", "0"):
        await db.set_flood(message.chat.id, 0)
        return await message.reply_text("🛡 <b>Anti-Flood disabled for this chat.</b>", quote=True)

    try:
        limit = int(val)
        if limit < 3:
            limit = 3
        elif limit > 30:
            limit = 30
        await db.set_flood(message.chat.id, limit)
        await message.reply_text(f"🛡 <b>Anti-Flood limit set to {limit} messages per 5 seconds.</b>", quote=True)
    except ValueError:
        await message.reply_text("Please provide a valid numeric limit (e.g. 5).")


@app.on_message(filters.group & ~filters.me, group=13)
async def flood_watcher(_, message: types.Message):
    if not message.from_user:
        return

    limit = await db.get_flood(message.chat.id)
    if not limit or limit <= 0:
        return

    if await is_admin(message.chat.id, message.from_user.id):
        return

    chat_id = message.chat.id
    user_id = message.from_user.id
    now = time.time()

    # Keep timestamps within last 5 seconds
    times = [t for t in user_msg_times[chat_id][user_id] if now - t < 5.0]
    times.append(now)
    user_msg_times[chat_id][user_id] = times

    if len(times) > limit:
        user_msg_times[chat_id][user_id].clear()
        try:
            permissions = types.ChatPermissions(can_send_messages=False)
            await message.chat.restrict_member(user_id, permissions=permissions)
            await message.reply_text(f"⚠️ {message.from_user.mention} <b>muted for flooding the chat!</b>")
        except Exception:
            pass
