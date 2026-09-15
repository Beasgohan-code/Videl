# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Seek & SeekBack Command

from pyrogram import filters, types
from videl import anon, app, db, lang, queue
from videl.helpers._admins import can_manage_vc


@app.on_message(filters.command(["seek", "seekback", "cseek"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _seek(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text(m.lang["play_seek_usage"].format(m.command[0]))

    try:
        to_seek = int(m.command[1])
    except ValueError:
        return await m.reply_text(m.lang["play_seek_usage"].format(m.command[0]))

    if to_seek < 10:
        return await m.reply_text(m.lang["play_seek_min"])

    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    if not await db.playing(m.chat.id):
        return await m.reply_text(m.lang["play_already_paused"])

    media = queue.get_current(m.chat.id)
    if not media or not media.duration_sec:
        return await m.reply_text(m.lang["play_seek_no_dur"])

    sent = await m.reply_text(m.lang["play_seeking"])
    if m.command[0] in ("seekback", "cseekback"):
        stype = m.lang["backward"]
        start_from = max(1, media.time - to_seek)
    else:
        stype = m.lang["forward"]
        start_from = media.time + to_seek
        if start_from + 10 > media.duration_sec:
            start_from = max(1, media.duration_sec - 5)

    await anon.play_media(m.chat.id, sent, media, start_from)
    media.time = start_from
    await sent.edit_text(
        m.lang["play_seeked"].format(stype, start_from, m.from_user.mention)
    )
