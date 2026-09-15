# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Queue Shuffle Command

from pyrogram import filters, types
from videl import app, db, lang, queue
from videl.helpers._admins import can_manage_vc


@app.on_message(filters.command(["shuffle", "cshuffle"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _shuffle(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    shuffled = queue.shuffle(m.chat.id)
    if not shuffled:
        return await m.reply_text("❌ <b>Not enough tracks in queue to shuffle!</b> (Need at least 2 tracks in queue)")

    await m.reply_text(f"🔀 <b>Queue successfully shuffled by {m.from_user.mention}!</b>")
