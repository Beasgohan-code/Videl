# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Interactive Search Plugin

try:
    from py_yt import VideosSearch
except ImportError:
    from py_yt_search import VideosSearch

from pyrogram import filters, types
from videl import app
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["search", "ytsearch"]) & ~app.bl_users)
async def search_cmd(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/search [query]</code>")

    query = " ".join(message.command[1:])
    sent = await message.reply_text(f"🔍 <i>Searching YouTube for:</i> <b>{query}</b>...")

    try:
        search = VideosSearch(query, limit=5)
        results = (await search.next()).get("result", [])
        if not results:
            return await sent.edit_text("❌ <b>No results found.</b>")

        text = f"🔍 <b><u>Top YouTube Results for:</u></b> <i>{query}</i>\n\n<blockquote expandable>"
        buttons_list = []

        for idx, item in enumerate(results, 1):
            title = item.get("title", "Unknown")[:40]
            duration = item.get("duration", "00:00")
            link = item.get("link", "")
            video_id = item.get("id", "")
            channel = item.get("channel", {}).get("name", "Unknown")

            text += f"<b>{idx}.</b> <a href='{link}'>{title}</a>\n    ⏱ <code>{duration}</code> • {channel}\n\n"
            buttons_list.append([
                styled_button(text=f"▶️ Play #{idx}", callback_data=f"ytsearch_play {video_id}", style=ButtonStyle.PRIMARY),
                styled_button(text=f"📥 Download #{idx}", callback_data=f"ytsearch_dl {video_id}", style=ButtonStyle.DEFAULT),
            ])

        text += "</blockquote>"
        buttons_list.append([
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER)
        ])

        await sent.edit_text(text, reply_markup=types.InlineKeyboardMarkup(buttons_list), disable_web_page_preview=True)
    except Exception as ex:
        await sent.edit_text(f"❌ <b>Search error:</b> <code>{ex}</code>")
