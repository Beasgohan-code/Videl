# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Smart AutoPlay & AI DJ Recommendation Engine

import random
from pyrogram import filters, types
from videl import anon, app, db, lang, queue, yt
from videl.helpers._admins import can_manage_vc
from videl.helpers._dataclass import Track

autodj_enabled = {}


async def fetch_recommended_track(chat_id: int, last_title: str) -> Track | None:
    """Finds next recommended song based on the last played song title."""
    try:
        clean_query = f"{last_title} related mix songs"
        track = await yt.search(clean_query, 0)
        return track
    except Exception:
        return None


@app.on_message(filters.command(["autodj", "autoplay", "endless"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def toggle_autodj(_, message: types.Message):
    chat_id = message.chat.id
    if len(message.command) < 2 or message.command[1].lower() not in ("on", "off"):
        current = autodj_enabled.get(chat_id, False)
        return await message.reply_text(
            f"🎧 <b>Smart AutoPlay / AI DJ:</b> <code>{'Enabled' if current else 'Disabled'}</code>\n\n"
            "When enabled, Videl automatically fetches and streams recommended related songs when your queue runs out!\n"
            "• <code>/autodj on</code> - Enable endless smart radio\n"
            "• <code>/autodj off</code> - Disable autoplay",
            quote=True,
        )

    enable = message.command[1].lower() == "on"
    autodj_enabled[chat_id] = enable
    await message.reply_text(f"🎧 <b>Smart AutoPlay / AI DJ is now:</b> <code>{'Enabled' if enable else 'Disabled'}</code>", quote=True)


@app.on_message(filters.command(["recommend", "suggest", "radiomix"]) & filters.group & ~app.bl_users)
async def recommend_cmd(_, message: types.Message):
    chat_id = message.chat.id
    media = queue.get_current(chat_id)

    if not media:
        return await message.reply_text("Play a song first to get AI DJ recommendations!", quote=True)

    sent = await message.reply_text(f"✨ <i>Finding AI DJ song recommendations based on:</i> <b>{media.title}</b>...")
    rec = await fetch_recommended_track(chat_id, media.title)

    if not rec:
        return await sent.edit_text("❌ Could not find suitable recommendations.")

    rec.user = message.from_user.mention
    pos = queue.add(chat_id, rec)
    await sent.edit_text(
        f"🎧 <b>AI DJ Recommendation Added to Queue!</b>\n\n"
        f"🎵 <b>Track:</b> <a href='{rec.url}'>{rec.title}</a> (<code>{rec.duration}</code>)\n"
        f"📋 <b>Queue Position:</b> #{pos + 1}"
    )
