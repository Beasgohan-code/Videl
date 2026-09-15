# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Telegram Stars & Collectible Gifts Plugin (Bot API 8.x/9.x/10.x)

from pyrogram import filters, types
from videl import app
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["gifts", "stargifts", "gift"]) & ~app.bl_users)
async def gifts_handler(_, message: types.Message):
    target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    name = target_user.first_name if target_user else "User"

    keyboard = types.InlineKeyboardMarkup([
        [
            styled_button(text="🎁 Send Telegram Gift", url=f"https://t.me/{app.username}?start=gift", style=ButtonStyle.PRIMARY),
            styled_button(text="⭐️ Send Stars", callback_data="stars", style=ButtonStyle.SUCCESS),
        ],
        [
            styled_button(text="💬 Support Community", url="https://t.me/BeasgohanSupport", style=ButtonStyle.DEFAULT),
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
        ]
    ])

    caption = (
        f"🎁 <b><u>Telegram Star Gifts & Collectibles</u></b>\n\n"
        f"👤 <b>Target:</b> {target_user.mention}\n"
        f"⭐️ <b>Collectibles API:</b> Bot API 10.x Enabled\n\n"
        f"You can send digital collectible gifts, stickers, and Telegram Stars to express your appreciation!"
    )

    await message.reply_text(caption, reply_markup=keyboard, quote=True)
