# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Shazam & Audio Recognition Plugin

import os
import asyncio
import aiohttp
from pyrogram import filters, types
from videl import app, logger
from videl.helpers.button_style import styled_button, ButtonStyle


async def recognize_audio(file_path: str):
    """Recognize song from audio file using Shazam / AudD API or fingerprinting."""
    try:
        # Extract audio chunk using FFmpeg
        sample_path = f"{file_path}_sample.mp3"
        proc = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i '{file_path}' -t 12 -vn -acodec libmp3lame -ar 44100 -ac 2 '{sample_path}'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()

        if not os.path.exists(sample_path):
            sample_path = file_path

        # Query public recognition endpoints
        data = None
        async with aiohttp.ClientSession() as session:
            with open(sample_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("file", f, filename="audio.mp3")
                async with session.post("https://api.audd.io/findLyrics/?return=timecode,spotify", data=form, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    if resp.status == 200:
                        res_json = await resp.json()
                        if res_json.get("status") == "success" and res_json.get("result"):
                            data = res_json["result"][0]

        if os.path.exists(sample_path) and sample_path != file_path:
            os.remove(sample_path)

        return data
    except Exception as ex:
        logger.debug(f"Shazam recognition error: {ex}")
        return None


@app.on_message(filters.command(["shazam", "identify", "whatsong", "findsong"]) & ~app.bl_users)
async def shazam_handler(_, message: types.Message):
    target = message.reply_to_message
    if not target or not (target.audio or target.voice or target.video or target.video_note):
        return await message.reply_text("Reply to an audio, voice note, or video file with <code>/shazam</code> to identify the song!")

    sent = await message.reply_text("🎧 <i>Listening and identifying audio with Shazam...</i>")
    os.makedirs("downloads", exist_ok=True)
    temp_file = f"downloads/shazam_{message.id}.mp3"

    try:
        await target.download(file_name=temp_file)
        result = await recognize_audio(temp_file)

        if not result:
            return await sent.edit_text("❌ <b>Could not recognize the song.</b> Make sure the music is clear and try again.")

        title = result.get("title", "Unknown Title")
        artist = result.get("artist", "Unknown Artist")
        album = result.get("album", "Unknown Album")
        lyrics = result.get("lyrics", "")

        text = (
            f"🎵 <b><u>Song Identified!</u></b>\n\n"
            f"• <b>Title:</b> {title}\n"
            f"• <b>Artist:</b> {artist}\n"
            f"• <b>Album:</b> {album}\n\n"
        )
        if lyrics:
            text += f"<blockquote expandable><b>Lyrics:</b>\n{lyrics[:1000]}...</blockquote>"

        search_query = f"{title} {artist}"
        buttons = [
            [
                styled_button(text="▶️ Stream in VC", callback_data=f"ytsearch_play {title}", style=ButtonStyle.PRIMARY),
                styled_button(text="📥 Download MP3", callback_data=f"ytsearch_dl {title}", style=ButtonStyle.DEFAULT),
            ],
            [
                styled_button(text="🔍 YouTube Search", url=f"https://youtube.com/results?search_query={title}+{artist}"),
                styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
            ]
        ]
        await sent.edit_text(text, reply_markup=types.InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    except Exception as ex:
        await sent.edit_text(f"❌ <b>Error:</b> <code>{ex}</code>")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
