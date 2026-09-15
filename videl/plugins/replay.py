# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Replay Command

from pyrogram import filters, types
from videl import anon, app, db, lang, queue
from videl.helpers._admins import can_manage_vc


@app.on_message(filters.command(["replay", "creplay"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _replay(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    media = queue.get_current(m.chat.id)
    if not media:
        return await m.reply_text(m.lang["not_playing"])

    media.user = m.from_user.mention if m.from_user else "Anonymous"
    await anon.replay(m.chat.id)
    await m.reply_text(m.lang["play_replayed"].format(m.from_user.mention))
