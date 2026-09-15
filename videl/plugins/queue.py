# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Queue Viewer Command

from pyrogram import filters, types
from videl import app, config, db, lang, queue, thumb
from videl.helpers._dataclass import Track
from videl.helpers._inline import buttons


@app.on_message(filters.command(["queue", "playing", "cqueue", "player"]) & filters.group & ~app.bl_users)
@lang.language()
async def _queue_func(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    _reply = await m.reply_text(m.lang["queue_fetching"])
    q_list = queue.get_queue(m.chat.id)
    if not q_list:
        return await _reply.edit_text(m.lang["not_playing"])

    _media = q_list[0]
    _thumb = (
        await thumb.generate(_media)
        if isinstance(_media, Track)
        else config.DEFAULT_THUMB
    ) if config.THUMB_GEN else None

    _text = m.lang["queue_curr"].format(
        _media.url,
        _media.title[:50],
        _media.duration,
        _media.user or "Anonymous",
    )

    remaining_queue = q_list[1:]
    if remaining_queue:
        _text += "<blockquote expandable>"
        for i, media in enumerate(remaining_queue, start=1):
            if i > 15:
                _text += f"<i>... and {len(remaining_queue) - 15} more tracks</i>\n"
                break
            _text += m.lang["queue_item"].format(i + 1, media.title, media.duration)
        _text += "</blockquote>"

    _playing = await db.playing(m.chat.id)
    _buttons = buttons.queue_markup(
        m.chat.id,
        m.lang["playing"] if _playing else m.lang["paused"],
        _playing,
    )

    if _thumb:
        try:
            await _reply.edit_media(
                media=types.InputMediaPhoto(media=_thumb, caption=_text),
                reply_markup=_buttons,
            )
        except Exception:
            await _reply.edit_text(text=_text, reply_markup=_buttons)
    else:
        await _reply.edit_text(text=_text, reply_markup=_buttons)
