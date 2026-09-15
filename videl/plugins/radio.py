# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl 24/7 Curated Live Radio & Streams Plugin

from pyrogram import filters, types
from videl import anon, app, db, lang, queue
from videl.helpers._admins import can_manage_vc
from videl.helpers._dataclass import Media
from videl.helpers.button_style import styled_button, ButtonStyle

RADIO_STATIONS = {
    "lofi": ("☕ Lofi Hip Hop (24/7)", "https://stream.zeno.fm/f3wvbbqmdg8uv"),
    "synth": ("🌆 Synthwave / Retro", "https://stream.nightride.fm/nightride.m4a"),
    "chill": ("🍃 Chillhop Relax", "https://stream.zeno.fm/0r0xa792kwzuv"),
    "anime": ("🌸 Anime Hits & OST", "https://stream.zeno.fm/79u9z98u2tzuv"),
    "edm": ("⚡ EDM & Electro House", "https://stream.zeno.fm/f9w7zbbqmdg8u"),
    "jazz": ("🎷 Coffee & Smooth Jazz", "https://stream.zeno.fm/36v9z08u2tzuv"),
    "rock": ("🎸 Classic Rock Live", "https://stream.zeno.fm/wr2uv792kwzuv"),
    "pop": ("🌟 Top 40 Global Pop", "https://stream.zeno.fm/f1wvbbqmdg8uv"),
}


def radio_keyboard(chat_id: int):
    buttons = [
        [
            styled_button(text="☕ Lofi 24/7", callback_data=f"play_radio {chat_id} lofi", style=ButtonStyle.PRIMARY),
            styled_button(text="🌆 Synthwave", callback_data=f"play_radio {chat_id} synth", style=ButtonStyle.PRIMARY),
        ],
        [
            styled_button(text="🍃 Chillhop", callback_data=f"play_radio {chat_id} chill", style=ButtonStyle.PRIMARY),
            styled_button(text="🌸 Anime OST", callback_data=f"play_radio {chat_id} anime", style=ButtonStyle.PRIMARY),
        ],
        [
            styled_button(text="⚡ EDM Dance", callback_data=f"play_radio {chat_id} edm", style=ButtonStyle.PRIMARY),
            styled_button(text="🎷 Smooth Jazz", callback_data=f"play_radio {chat_id} jazz", style=ButtonStyle.PRIMARY),
        ],
        [
            styled_button(text="🎸 Classic Rock", callback_data=f"play_radio {chat_id} rock", style=ButtonStyle.PRIMARY),
            styled_button(text="🌟 Top 40 Pop", callback_data=f"play_radio {chat_id} pop", style=ButtonStyle.PRIMARY),
        ],
        [
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER)
        ]
    ]
    return types.InlineKeyboardMarkup(buttons)


@app.on_message(filters.command(["radio", "live", "radios"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def radio_cmd(_, message: types.Message):
    await message.reply_text(
        "📻 <b><u>Videl 24/7 Live Radio Stations</u></b>\n\n"
        "Choose a live streaming station below to start streaming immediately in the voice chat:",
        reply_markup=radio_keyboard(message.chat.id),
    )


@app.on_callback_query(filters.regex(r"^play_radio") & ~app.bl_users)
@can_manage_vc
async def play_radio_cb(_, query: types.CallbackQuery):
    _, chat_id_str, station_key = query.data.split()
    chat_id = int(chat_id_str)

    if station_key not in RADIO_STATIONS:
        return await query.answer("❌ Radio station not found!", show_alert=True)

    station_name, stream_url = RADIO_STATIONS[station_key]
    await query.answer(f"📻 Connecting to {station_name}...")

    media = Media(
        id=f"radio_{station_key}",
        title=station_name,
        duration="Live Radio 24/7",
        duration_sec=0,
        file_path=stream_url,
        message_id=query.message.id,
        url="https://zeno.fm",
        user=query.from_user.mention,
    )

    queue.clear(chat_id)
    queue.add(chat_id, media)
    await anon.play_media(chat_id, query.message, media)
