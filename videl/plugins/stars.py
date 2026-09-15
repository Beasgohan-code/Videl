# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Telegram Stars Tipping & Donation Invoices Plugin

from pyrogram import filters, types
from videl import app, bridge
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["stars", "tip", "donate", "star"]) & ~app.bl_users)
async def stars_handler(_, message: types.Message):
    stars_amount = 25
    if len(message.command) > 1 and message.command[1].isdigit():
        stars_amount = max(1, min(int(message.command[1]), 2500))

    sent_invoice = await bridge.send_star_invoice(
        chat_id=message.chat.id,
        title=f"Support {app.name} ⭐️",
        description=f"Send {stars_amount} Telegram Stars to support Videl's high-speed voice streaming infrastructure!",
        payload=f"tip_{message.from_user.id}_{stars_amount}",
        stars_amount=stars_amount,
    )

    if not sent_invoice:
        keyboard = types.InlineKeyboardMarkup([
            [
                styled_button(text="⭐️ Support on Telegram", url="https://t.me/BeasgohanSupport", style=ButtonStyle.PRIMARY),
                styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
            ]
        ])
        await message.reply_text(
            f"⭐️ <b><u>Support {app.name}</u></b>\n\n"
            "Thank you for loving Videl Music! Join our support community and help keep the streaming servers online.",
            reply_markup=keyboard,
            quote=True,
        )
