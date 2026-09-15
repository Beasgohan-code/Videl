# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Stop / End Command

from pyrogram import filters, types
from videl import anon, app, db, lang
from videl.helpers._admins import can_manage_vc


@app.on_message(filters.command(["stop", "end"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _stop(_, m: types.Message):
    if len(m.command) > 1:
        return

    call = await db.get_call(m.chat.id)
    await anon.stop(m.chat.id)
    if not call:
        return await m.reply_text(m.lang["not_playing"])

    await m.reply_text(m.lang["play_stopped"].format(m.from_user.mention))
