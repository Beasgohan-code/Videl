# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Rich Media Cards & Headings Generator Plugin

from pyrogram import filters, types
from videl import app
from videl.helpers.button_style import styled_button, ButtonStyle
from videl.helpers.rich_ui import render_table, render_quote_card, render_heading


@app.on_message(filters.command(["mediacard", "card", "richcard"]) & ~app.bl_users)
async def media_card_command(_, message: types.Message):
    target_msg = message.reply_to_message or message
    has_photo = bool(target_msg.photo)
    has_video = bool(target_msg.video)

    heading = "🌟 VIP SPOTLIGHT"
    if len(message.command) > 1:
        heading = message.text.split(None, 1)[1]

    table_data = render_table(
        ["Metric", "Status"],
        [
            ["Audio Quality", "HD Opus 320kbps"],
            ["Visual FX", "Active (Bot API 10.x)"],
            ["Bitrate", "48.0 kHz Dual Stereo"],
            ["Latency", "Ultra-Low (<15ms)"],
        ],
        style="box",
    )

    quote_block = render_quote_card(
        text="Music is the universal language of mankind.",
        author="Henry Wadsworth Longfellow",
        title="Quote of the Day",
    )

    card_text = (
        f"╔════════════════════════════════════╗\n"
        f"║  ✨ <b>{heading.upper()}</b>\n"
        f"╚════════════════════════════════════╝\n\n"
        f"🎧 <b>Engine:</b> Dual MTProto + Bot API 10.x Streamer\n\n"
        f"{table_data}\n"
        f"{quote_block}"
    )

    keyboard = types.InlineKeyboardMarkup([
        [
            styled_button(text="🎵 Stream in VC", callback_data="cb_nowplaying", style=ButtonStyle.PRIMARY),
            styled_button(text="📱 Mini App", callback_data="help", style=ButtonStyle.SUCCESS),
        ],
        [
            styled_button(text="💬 Support Community", url="https://t.me/BeasgohanSupport", style=ButtonStyle.DEFAULT),
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
        ]
    ])

    if has_photo:
        await message.reply_photo(
            photo=target_msg.photo.file_id,
            caption=card_text,
            reply_markup=keyboard,
            quote=True,
        )
    elif has_video:
        await message.reply_video(
            video=target_msg.video.file_id,
            caption=card_text,
            reply_markup=keyboard,
            quote=True,
        )
    else:
        await message.reply_text(
            card_text,
            reply_markup=keyboard,
            quote=True,
        )
