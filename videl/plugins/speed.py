# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Speed Control Command

from pyrogram import filters, types
from videl import app, db, lang
from videl.helpers._admins import can_manage_vc
from videl.helpers._inline import buttons


@app.on_message(filters.command(["speed", "playbackspeed", "cspeed"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _speed(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    current_speed = await db.get_speed(m.chat.id)
    await m.reply_text(
        f"⚡ <b>Current Playback Speed:</b> <code>{current_speed}x</code>\n\nChoose speed preset below:",
        reply_markup=buttons.speed_markup(m.chat.id, current_speed),
    )
