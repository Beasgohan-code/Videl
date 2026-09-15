# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Lyrics Plugin

from pyrogram import filters, types
from videl import app, db, lang, queue
from videl.helpers._utilities import fetch_lyrics


@app.on_message(filters.command(["lyrics", "lyric", "clyrics"]) & ~app.bl_users)
@lang.language()
async def _lyrics(_, m: types.Message):
    if len(m.command) >= 2:
        query = " ".join(m.command[1:])
    else:
        current = queue.get_current(m.chat.id) if await db.get_call(m.chat.id) else None
        if current:
            query = current.title
        else:
            return await m.reply_text("<b>Usage:</b> <code>/lyrics [song name]</code>")

    sent = await m.reply_text(f"🔍 <i>Searching lyrics for:</i> <b>{query}</b>...")
    lyrics = await fetch_lyrics(query)
    if not lyrics:
        return await sent.edit_text(f"❌ <i>No lyrics found for:</i> <b>{query}</b>")

    text = f"📜 <b><u>Lyrics for {query}</u></b>\n\n<blockquote expandable>{lyrics[:3900]}</blockquote>"
    await sent.edit_text(text)
