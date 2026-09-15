# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Personal & Group Playlists Manager

from pyrogram import filters, types
from videl import anon, app, db, lang, queue, yt
from videl.helpers._dataclass import Track
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["playlist", "myplaylist", "cplaylist"]) & ~app.bl_users)
async def view_playlist(_, message: types.Message):
    user_id = message.from_user.id
    tracks = await db.get_playlist(user_id)

    if not tracks:
        return await message.reply_text(
            "<b>Your personal playlist is currently empty!</b>\n\n"
            "Use <code>/addplaylist [song name / YouTube link]</code> or reply to a song to add tracks.",
            quote=True,
        )

    text = f"✨ <b><u>Your Personal Playlist ({len(tracks)} tracks)</u></b>\n\n<blockquote expandable>"
    for idx, t in enumerate(tracks[:20], 1):
        text += f"<b>{idx}.</b> <a href='{t.get('url', '')}'>{t.get('title', 'Unknown')[:35]}</a> (<code>{t.get('duration', '00:00')}</code>)\n"
    if len(tracks) > 20:
        text += f"\n<i>... and {len(tracks) - 20} more tracks</i>"
    text += "</blockquote>"

    buttons = [
        [
            styled_button(text="▶️ Play Entire Playlist", callback_data=f"play_user_playlist {user_id}", style=ButtonStyle.PRIMARY),
            styled_button(text="🗑 Clear Playlist", callback_data=f"clear_user_playlist {user_id}", style=ButtonStyle.DANGER),
        ],
        [
            styled_button(text="❌ Close", callback_data="help close", style=ButtonStyle.DEFAULT)
        ]
    ]

    await message.reply_text(text, reply_markup=types.InlineKeyboardMarkup(buttons), quote=True, disable_web_page_preview=True)


@app.on_message(filters.command(["addplaylist", "saveplaylist"]) & ~app.bl_users)
async def add_playlist(_, message: types.Message):
    user_id = message.from_user.id
    current_tracks = await db.get_playlist(user_id)

    if len(current_tracks) >= 50:
        return await message.reply_text("❌ <b>Playlist limit reached!</b> (Maximum 50 tracks per playlist)")

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("<b>Usage:</b> <code>/addplaylist [song name / link]</code> or reply to a music track.")

    query = " ".join(message.command[1:]) if len(message.command) > 1 else message.reply_to_message.text
    sent = await message.reply_text(f"🔍 <i>Searching song to add:</i> <b>{query}</b>...")

    track = await yt.search(query, message.id)
    if not track:
        return await sent.edit_text("❌ <b>Song not found on YouTube.</b>")

    track_dict = {
        "id": track.id,
        "title": track.title,
        "url": track.url,
        "duration": track.duration,
        "duration_sec": track.duration_sec,
        "thumbnail": track.thumbnail,
    }
    await db.add_to_playlist(user_id, track_dict)
    await sent.edit_text(f"✅ <b>Added to your playlist:</b> <a href='{track.url}'>{track.title}</a> (<code>{track.duration}</code>)")


@app.on_message(filters.command(["delplaylist", "rmplaylist"]) & ~app.bl_users)
async def rm_playlist(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/delplaylist [track ID / index number]</code>")

    user_id = message.from_user.id
    arg = message.command[1]
    tracks = await db.get_playlist(user_id)

    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(tracks):
            track_to_del = tracks[idx]
            await db.remove_from_playlist(user_id, track_to_del["id"])
            return await message.reply_text(f"🗑 <b>Removed track #{arg} from playlist:</b> {track_to_del.get('title')}")

    await db.remove_from_playlist(user_id, arg)
    await message.reply_text(f"🗑 <b>Removed track from playlist.</b>")


@app.on_message(filters.command(["playplaylist", "streamplaylist"]) & filters.group & ~app.bl_users)
async def play_playlist_cmd(_, message: types.Message):
    user_id = message.from_user.id
    tracks = await db.get_playlist(user_id)

    if not tracks:
        return await message.reply_text("❌ <b>Your playlist is empty!</b> Use <code>/addplaylist</code> first.")

    sent = await message.reply_text(f"⏳ <i>Importing {len(tracks)} songs from your playlist...</i>")
    mention = message.from_user.mention

    first_track = None
    for i, t_data in enumerate(tracks):
        track_obj = Track(
            id=t_data["id"],
            title=t_data["title"],
            duration=t_data.get("duration", "00:00"),
            duration_sec=t_data.get("duration_sec", 0),
            url=t_data.get("url", f"https://youtube.com/watch?v={t_data['id']}"),
            thumbnail=t_data.get("thumbnail"),
            user=mention,
        )
        if i == 0 and not await db.get_call(message.chat.id):
            first_track = track_obj
        else:
            queue.add(message.chat.id, track_obj)

    if first_track:
        first_track.message_id = sent.id
        first_track.file_path = await yt.download(first_track.id)
        await anon.play_media(chat_id=message.chat.id, message=sent, media=first_track)
    else:
        await sent.edit_text(f"📋 <b>Enqueued {len(tracks)} tracks from your personal playlist!</b>")


@app.on_callback_query(filters.regex(r"^(play|clear)_user_playlist") & ~app.bl_users)
async def playlist_callback(_, query: types.CallbackQuery):
    action, user_id_str = query.data.split()
    user_id = int(user_id_str)

    if query.from_user.id != user_id:
        return await query.answer("❌ This is not your playlist!", show_alert=True)

    if action == "clear_user_playlist":
        await db.clear_playlist(user_id)
        await query.answer("🗑 Playlist cleared successfully!", show_alert=True)
        return await query.edit_message_text("🗑 <b>Your personal playlist has been cleared.</b>")

    elif action == "play_user_playlist":
        tracks = await db.get_playlist(user_id)
        if not tracks:
            return await query.answer("❌ Playlist is empty!", show_alert=True)

        await query.answer("⚡ Enqueueing your playlist...", show_alert=True)
        mention = query.from_user.mention

        for t_data in tracks:
            track_obj = Track(
                id=t_data["id"],
                title=t_data["title"],
                duration=t_data.get("duration", "00:00"),
                duration_sec=t_data.get("duration_sec", 0),
                url=t_data.get("url", f"https://youtube.com/watch?v={t_data['id']}"),
                thumbnail=t_data.get("thumbnail"),
                user=mention,
            )
            queue.add(query.message.chat.id, track_obj)

        if not await db.get_call(query.message.chat.id):
            curr = queue.get_next(query.message.chat.id)
            if curr:
                curr.file_path = await yt.download(curr.id)
                await anon.play_media(query.message.chat.id, query.message, curr)
        else:
            await query.message.reply_text(f"📋 <b>Enqueued {len(tracks)} tracks from playlist!</b>")
