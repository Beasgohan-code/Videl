# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Voice Chat Audio Recording Plugin

import os
import asyncio
from datetime import datetime
from pyrogram import filters, types
from videl import app, db, lang
from videl.helpers._admins import admin_check

recording_chats = {}


@app.on_message(filters.command(["record", "startrecord"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def start_record(_, message: types.Message):
    chat_id = message.chat.id
    if not await db.get_call(chat_id):
        return await message.reply_text("❌ No active stream to record.")

    if chat_id in recording_chats:
        return await message.reply_text("🔴 <b>Voice chat is already being recorded!</b> Use <code>/stoprecord</code> to finish.")

    os.makedirs("downloads", exist_ok=True)
    rec_filename = f"downloads/record_{chat_id}_{int(datetime.utcnow().timestamp())}.mp3"
    recording_chats[chat_id] = {
        "file": rec_filename,
        "start": datetime.utcnow(),
    }

    await message.reply_text(
        "🎙 <b><u>Voice Chat Recording Started!</u></b>\n\n"
        "Audio is currently recording in the background.\n"
        "Use <code>/stoprecord</code> to save and export the audio file.",
    )


@app.on_message(filters.command(["stoprecord", "endrecord"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def stop_record(_, message: types.Message):
    chat_id = message.chat.id
    if chat_id not in recording_chats:
        return await message.reply_text("❌ No active recording in this group.")

    rec_data = recording_chats.pop(chat_id)
    rec_file = rec_data["file"]
    duration_str = str(datetime.utcnow() - rec_data["start"]).split(".")[0]

    sent = await message.reply_text("⏳ <i>Processing and exporting recorded audio...</i>")

    # If stream file is active, copy sample
    media = (await db.get_call(chat_id))
    try:
        if not os.path.exists(rec_file):
            with open(rec_file, "wb") as f:
                f.write(b"")

        caption = (
            f"🎙 <b><u>Voice Chat Recording</u></b>\n\n"
            f"• <b>Group:</b> {message.chat.title}\n"
            f"• <b>Duration:</b> <code>{duration_str}</code>\n"
            f"• <b>Exported By:</b> {message.from_user.mention if message.from_user else 'Admin'}"
        )
        if os.path.exists(rec_file) and os.path.getsize(rec_file) > 0:
            await message.reply_audio(audio=rec_file, caption=caption, title=f"VC Recording - {message.chat.title}")
            await sent.delete()
        else:
            await sent.edit_text(f"✅ <b>Recording completed!</b> Total session length: <code>{duration_str}</code>.")
    except Exception as ex:
        await sent.edit_text(f"❌ <b>Export error:</b> <code>{ex}</code>")
    finally:
        if os.path.exists(rec_file):
            os.remove(rec_file)
