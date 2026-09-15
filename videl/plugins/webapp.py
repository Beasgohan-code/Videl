# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl WebApp & Mini App Controller Plugin

from pyrogram import filters, types
from videl import app, queue
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["webapp", "miniapp", "app", "webplayer"]) & ~app.bl_users)
async def webapp_handler(_, message: types.Message):
    # WebApp URL endpoint for Videl Mini App Player
    webapp_url = f"https://t.me/{app.username}/player"

    keyboard = types.InlineKeyboardMarkup([
        [
            types.InlineKeyboardButton(
                text="📱 Launch Videl Mini App",
                web_app=types.WebAppInfo(url=f"https://telegram.org")
            )
        ],
        [
            styled_button(text="🎵 Current Track", callback_data="cb_nowplaying", style=ButtonStyle.PRIMARY),
            styled_button(text="📜 Live Queue", callback_data="cb_queue", style=ButtonStyle.SECONDARY),
        ],
        [
            styled_button(text="✨ Support Community", url="https://t.me/BeasgohanSupport", style=ButtonStyle.SUCCESS),
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
        ]
    ])

    current = queue.get_current(message.chat.id)
    title = current.title if current else "No Track Playing"

    caption = (
        f"📱 <b><u>{app.name} Interactive Mini App</u></b>\n\n"
        f"Control group playback, explore endless radio, customize audio equalizer & visual effects, and browse your personal playlists in the Telegram Mini App!\n\n"
        f"🎧 <b>Active Audio:</b> <code>{title}</code>\n"
        f"⚡ <b>Engine:</b> Dual MTProto + Bot API 10.x"
    )

    await message.reply_text(caption, reply_markup=keyboard, quote=True)
