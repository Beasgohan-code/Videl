# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Callback Query Router

import re
from pyrogram import errors, filters, types
from videl import anon, app, db, lang, queue, tg, yt
from videl.helpers._admins import admin_check, can_manage_vc
from videl.helpers._inline import buttons
from videl.helpers._utilities import fetch_lyrics


@app.on_callback_query(filters.regex("cancel_dl") & ~app.bl_users)
@lang.language()
async def cancel_dl(_, query: types.CallbackQuery):
    await query.answer()
    await tg.cancel(query)


@app.on_callback_query(filters.regex("controls") & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _controls(_, query: types.CallbackQuery):
    args = query.data.split()
    action = args[1]
    chat_id = int(args[2])
    user = query.from_user.mention if query.from_user else "Anonymous"
    qaction = len(args) == 4

    if not await db.get_call(chat_id):
        try:
            return await query.answer(query.lang["not_playing"], show_alert=True)
        except errors.QueryIdInvalid:
            try:
                await query.message.delete()
            except Exception:
                pass
            return

    if action == "status":
        return await query.answer("⚡ Videl Music Stream is Active!")

    await query.answer(query.lang["processing"])
    status = None
    reply = ""

    if action == "pause":
        if not await db.playing(chat_id):
            return await query.answer(query.lang["play_already_paused"], show_alert=True)
        await anon.pause(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["paused"], False)
            )
        status = query.lang["paused"]
        reply = query.lang["play_paused"].format(user)

    elif action == "resume":
        if await db.playing(chat_id):
            return await query.answer(query.lang["play_not_paused"], show_alert=True)
        await anon.resume(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["playing"], True)
            )
        reply = query.lang["play_resumed"].format(user)

    elif action == "skip":
        await anon.play_next(chat_id)
        status = query.lang["skipped"]
        reply = query.lang["play_skipped"].format(user)

    elif action == "stop":
        await anon.stop(chat_id)
        status = query.lang["stopped"]
        reply = query.lang["play_stopped"].format(user)

    elif action == "replay":
        media = queue.get_current(chat_id)
        if media:
            media.user = user
        await anon.replay(chat_id)
        status = query.lang["replayed"]
        reply = query.lang["play_replayed"].format(user)

    elif action == "seekback":
        media = queue.get_current(chat_id)
        if media and media.duration_sec:
            start_from = max(1, media.time - 10)
            await anon.play_media(chat_id, query.message, media, start_from)
            media.time = start_from
            return await query.answer(f"⏮ Seeked backward 10s to {start_from}s", show_alert=False)
        return await query.answer("Cannot seek this stream", show_alert=True)

    elif action == "loop":
        curr = await db.get_loop(chat_id)
        nxt = 3 if curr == 0 else (5 if curr == 3 else (0 if curr == 5 else 0))
        await db.set_loop(chat_id, nxt)
        msg_loop = f"🔁 Loop set to {nxt} times!" if nxt > 0 else "🔁 Loop disabled!"
        return await query.answer(msg_loop, show_alert=True)

    elif action == "shuffle":
        shuffled = queue.shuffle(chat_id)
        if shuffled:
            return await query.answer("🔀 Queue shuffled successfully!", show_alert=True)
        return await query.answer("❌ Queue needs at least 2 tracks to shuffle", show_alert=True)

    elif action == "vol_menu":
        curr_vol = await db.get_volume(chat_id)
        return await query.edit_message_reply_markup(reply_markup=buttons.volume_markup(chat_id, curr_vol))

    elif action == "vol":
        vol = int(args[3])
        await anon.change_volume(chat_id, vol)
        return await query.answer(f"🔊 Volume set to {vol}%", show_alert=True)

    elif action == "speed_menu":
        curr_spd = await db.get_speed(chat_id)
        return await query.edit_message_reply_markup(reply_markup=buttons.speed_markup(chat_id, curr_spd))

    elif action == "spd":
        spd = float(args[3])
        await db.set_speed(chat_id, spd)
        return await query.answer(f"⚡ Speed set to {spd}x", show_alert=True)

    elif action == "lyrics":
        media = queue.get_current(chat_id)
        if media:
            lyrics = await fetch_lyrics(media.title)
            if lyrics:
                try:
                    await query.message.reply_text(
                        f"📜 <b>Lyrics for {media.title}:</b>\n\n<blockquote expandable>{lyrics[:3900]}</blockquote>"
                    )
                    return await query.answer("📜 Lyrics sent in chat!")
                except Exception:
                    pass
        return await query.answer("❌ No lyrics found for current track", show_alert=True)

    elif action == "back":
        is_p = await db.playing(chat_id)
        return await query.edit_message_reply_markup(reply_markup=buttons.controls(chat_id, is_playing=is_p))

    elif action == "force":
        pos, media = queue.check_item(chat_id, args[3])
        if not media or pos == -1:
            return await query.edit_message_text(query.lang["play_expired"])

        curr_med = queue.get_current(chat_id)
        m_id = curr_med.message_id if curr_med else None
        queue.force_add(chat_id, media, remove=pos)
        try:
            if m_id and media.message_id:
                await app.delete_messages(chat_id=chat_id, message_ids=[m_id, media.message_id], revoke=True)
            media.message_id = None
        except Exception:
            pass

        msg = await app.send_message(chat_id=chat_id, text=query.lang["play_next"])
        if not media.file_path:
            media.file_path = await yt.download(media.id, video=media.video)
        media.message_id = msg.id
        return await anon.play_media(chat_id, msg, media)

    try:
        if action in ["skip", "replay", "stop"]:
            await query.message.reply_text(reply, quote=False)
            await query.message.delete()
        else:
            caption_or_text = query.message.caption.html if query.message.caption else query.message.text.html
            mtext = re.sub(r"\n\n<blockquote>.*?</blockquote>", "", caption_or_text, flags=re.DOTALL)
            is_p = await db.playing(chat_id)
            keyboard = buttons.controls(chat_id, status=status if action != "resume" else None, is_playing=is_p)
            await query.edit_message_text(f"{mtext}\n\n<blockquote>{reply}</blockquote>", reply_markup=keyboard)
    except Exception:
        pass


@app.on_callback_query(filters.regex("help") & ~app.bl_users)
@lang.language()
async def _help_cb(_, query: types.CallbackQuery):
    data = query.data.split()
    if len(data) == 1:
        return await query.answer(url=f"https://t.me/{app.username}?start=help")

    if data[1] == "back":
        return await query.edit_message_text(
            text=query.lang["help_menu"], reply_markup=buttons.help_markup(query.lang)
        )
    elif data[1] == "close":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            pass
        return

    help_key = f"help_{data[1]}"
    help_text = query.lang.get(help_key, f"Help section: {data[1]}")
    await query.edit_message_text(
        text=help_text,
        reply_markup=buttons.help_markup(query.lang, True),
    )


@app.on_callback_query(filters.regex("settings") & ~app.bl_users)
@lang.language()
@admin_check
async def _settings_cb(_, query: types.CallbackQuery):
    cmd = query.data.split()
    if len(cmd) == 1:
        return await query.answer()
    await query.answer(query.lang["processing"])

    chat_id = query.message.chat.id
    _admin = await db.get_play_mode(chat_id)
    _delete = await db.get_cmd_delete(chat_id)
    _language = await db.get_lang(chat_id)

    if cmd[1] == "delete":
        _delete = not _delete
        await db.set_cmd_delete(chat_id, _delete)
    elif cmd[1] == "play":
        _admin = not _admin
        await db.set_play_mode(chat_id, _admin)

    await query.edit_message_reply_markup(
        reply_markup=buttons.settings_markup(
            query.lang,
            _admin,
            _delete,
            _language,
            chat_id,
        )
    )
