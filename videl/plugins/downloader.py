# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl High-Speed Video & Song Downloader Plugin

import os
import asyncio
import yt_dlp
from typing import Optional
from pyrogram import filters, types
from pyrogram.enums import ChatType
from videl import app, config, logger
from videl.helpers.button_style import styled_button, ButtonStyle
from videl.helpers.rich_message import RichMessage

try:
    from py_yt import VideosSearch
except ImportError:
    from youtubesearchpython import VideosSearch


async def get_search_results(query: str):
    try:
        search = VideosSearch(query, limit=1)
        res = await search.next() if asyncio.iscoroutinefunction(search.next) else search.result()
        results = res.get("result", [])
        if results:
            return {
                "id": results[0].get("id"),
                "link": results[0].get("link"),
                "title": results[0].get("title", "Audio Stream"),
                "duration": results[0].get("duration", "00:00"),
                "thumbnail": results[0].get("thumbnails", [{}])[-1].get("url", "").split("?")[0],
            }
    except Exception:
        pass
    return None


@app.on_message(filters.command(["song", "vsong", "video", "ytmp3", "ytmp4", "download", "music"]) & ~app.bl_users)
async def download_media(_, message: types.Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "<b>Usage:</b>\n"
            "• <code>/song [song name / URL]</code> (Download High Quality MP3)\n"
            "• <code>/video [video name / URL]</code> (Download HD 720p/1080p MP4)",
            quote=True,
        )

    cmd = message.command[0].lower()
    is_video = cmd in ("video", "vsong", "ytmp4")
    query = " ".join(message.command[1:]) if len(message.command) > 1 else message.reply_to_message.text

    status_msg = await message.reply_text(f"🔍 <i>Searching {'video' if is_video else 'audio'} for:</i> <b>{query}</b>...")

    # Fast search
    url = query if ("youtube.com" in query or "youtu.be" in query) else None
    title = "Media Stream"
    duration = "00:00"
    thumb_url = config.DEFAULT_THUMB

    if not url:
        res = await get_search_results(query)
        if res:
            url = res["link"]
            title = res["title"]
            duration = res["duration"]
            thumb_url = res["thumbnail"]
        else:
            url = f"ytsearch:{query}"

    await status_msg.edit_text(f"⚡ <i>Downloading {'HD Video' if is_video else 'HQ Audio'} from YouTube...</i>")

    out_id = f"dl_{message.id}_{message.from_user.id if message.from_user else 0}"
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("cache", exist_ok=True)

    if is_video:
        file_path = f"downloads/{out_id}.mp4"
        ydl_opts = {
            "format": "bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": f"downloads/{out_id}.%(ext)s",
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,
        }
    else:
        file_path = f"downloads/{out_id}.mp3"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{out_id}.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,
        }

    def _run_dl():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            nonlocal title, duration
            if "entries" in info:
                info = info["entries"][0]
            title = info.get("title", title)
            dur_sec = info.get("duration", 0)
            if dur_sec:
                import time
                duration = time.strftime("%M:%S", time.gmtime(dur_sec))
            return info

    try:
        await asyncio.to_thread(_run_dl)
    except Exception as ex:
        logger.error(f"Downloader error: {ex}")
        return await status_msg.edit_text(f"❌ <b>Download failed:</b> <code>{ex}</code>")

    # Find resulting file
    target_file = None
    for ext in ["mp3", "mp4", "m4a", "webm", "mkv"]:
        candidate = f"downloads/{out_id}.{ext}"
        if os.path.exists(candidate):
            target_file = candidate
            break

    if not target_file or not os.path.exists(target_file):
        return await status_msg.edit_text("❌ <b>Could not locate downloaded media file.</b>")

    await status_msg.edit_text("📤 <i>Uploading to Telegram...</i>")

    caption = (
        f"<b>⚡ <u>Downloaded via {app.name}</u></b>\n\n"
        f"🎵 <b>Title:</b> <code>{title[:50]}</code>\n"
        f"⏱ <b>Duration:</b> <code>{duration}</code>\n"
        f"📁 <b>Format:</b> <code>{'MP4 Video (720p)' if is_video else 'MP3 Audio (320kbps)'}</code>\n"
        f"🙋‍♂️ <b>Requested By:</b> {message.from_user.mention if message.from_user else 'Anonymous'}"
    )

    yt_link = url if url.startswith("http") else f"https://youtube.com/results?search_query={query}"
    keyboard = types.InlineKeyboardMarkup([
        [
            styled_button(text="❐ Copy Link", copy_text=yt_link, style=ButtonStyle.PRIMARY),
            styled_button(text="🎥 YouTube", url=yt_link, style=ButtonStyle.DEFAULT),
        ]
    ])

    try:
        if is_video:
            await message.reply_video(
                video=target_file,
                caption=caption,
                duration=0,
                reply_markup=keyboard,
                quote=True,
            )
        else:
            await message.reply_audio(
                audio=target_file,
                caption=caption,
                title=title[:40],
                performer=app.name,
                reply_markup=keyboard,
                quote=True,
            )
        await status_msg.delete()
    except Exception as ex:
        logger.error(f"Failed to upload media: {ex}")
        await status_msg.edit_text(f"❌ <b>Upload failed:</b> <code>{ex}</code>")

    # Cleanup
    if os.path.exists(target_file):
        os.remove(target_file)
