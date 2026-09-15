# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot API 8.x/10.x Star Paid Media Plugin

from pyrogram import filters, types
from videl import app, bridge
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["paidmedia", "starmedia"]) & app.sudoers)
async def paid_media_handler(_, message: types.Message):
    if not message.reply_to_message or (not message.reply_to_message.photo and not message.reply_to_message.video):
        return await message.reply_text(
            "💎 <b><u>Bot API 8.x+ Telegram Star Paid Media</u></b>\n\n"
            "<b>Usage:</b> Reply to a photo or video with <code>/paidmedia [Star Price] [Optional Caption]</code>\n"
            "<i>Example:</i> <code>/paidmedia 10 Exclusive VIP Live Concert Recording! ⭐️</code>",
            quote=True,
        )

    star_count = 10
    caption = "💎 Exclusive Paid Media Content"

    if len(message.command) > 1 and message.command[1].isdigit():
        star_count = max(1, min(int(message.command[1]), 2500))
    if len(message.command) > 2:
        caption = message.text.split(None, 2)[2]

    # Send Star Invoiced Media Card with ButtonStyle
    keyboard = types.InlineKeyboardMarkup([
        [
            styled_button(text=f"⭐️ Unlock for {star_count} Stars", callback_data=f"stars", style=ButtonStyle.PRIMARY),
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
        ]
    ])

    if message.reply_to_message.photo:
        await app.send_photo(
            chat_id=message.chat.id,
            photo=message.reply_to_message.photo.file_id,
            caption=f"⭐️ <b><u>Telegram Stars Paid Content</u></b>\n\n{caption}\n\n<b>Price:</b> <code>{star_count} ⭐️ Stars</code>",
            reply_markup=keyboard,
            has_spoiler=True,
        )
    elif message.reply_to_message.video:
        await app.send_video(
            chat_id=message.chat.id,
            video=message.reply_to_message.video.file_id,
            caption=f"⭐️ <b><u>Telegram Stars Paid Content</u></b>\n\n{caption}\n\n<b>Price:</b> <code>{star_count} ⭐️ Stars</code>",
            reply_markup=keyboard,
            has_spoiler=True,
        )
