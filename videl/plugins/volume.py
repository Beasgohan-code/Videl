# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Volume Control Command

from pyrogram import filters, types
from videl import anon, app, db, lang
from videl.helpers._admins import can_manage_vc
from videl.helpers._inline import buttons


@app.on_message(filters.command(["volume", "vol", "cvolume", "cvol"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _volume(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    if len(m.command) < 2:
        current_vol = await db.get_volume(m.chat.id)
        return await m.reply_text(
            f"🔊 <b>Current Stream Volume:</b> <code>{current_vol}%</code>\n\nChoose a volume preset below:",
            reply_markup=buttons.volume_markup(m.chat.id, current_vol),
        )

    try:
        vol = int(m.command[1])
    except ValueError:
        return await m.reply_text("<b>Usage:</b> <code>/volume [1-200]</code>")

    if vol < 1:
        vol = 1
    elif vol > 200:
        vol = 200

    success = await anon.change_volume(m.chat.id, vol)
    if success:
        await m.reply_text(f"🔊 <b>Volume updated to:</b> <code>{vol}%</code>")
    else:
        await m.reply_text(f"🔊 <b>Volume set to:</b> <code>{vol}%</code>")
