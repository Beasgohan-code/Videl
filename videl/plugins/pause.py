# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Pause Command

from pyrogram import filters, types
from videl import anon, app, db, lang
from videl.helpers._admins import can_manage_vc
from videl.helpers._inline import buttons


@app.on_message(filters.command(["pause"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _pause(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    if not await db.playing(m.chat.id):
        return await m.reply_text(m.lang["play_already_paused"])

    await anon.pause(m.chat.id)
    await m.reply_text(
        text=m.lang["play_paused"].format(m.from_user.mention),
        reply_markup=buttons.controls(m.chat.id, is_playing=False),
    )
