# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Real-Time Audio DSP Effects & Equalizer Plugin

from pyrogram import filters, types
from videl import anon, app, db, lang, queue
from videl.helpers._admins import can_manage_vc
from videl.helpers._filters_dsp import DSP_PRESETS, get_dsp_ffmpeg_param
from videl.helpers.button_style import styled_button, ButtonStyle


def dsp_menu_markup(chat_id: int, current: str):
    buttons = [
        [
            styled_button(text="🔊 Bass Boost" + (" ✔️" if current == "bassboost" else ""), callback_data=f"dsp_set {chat_id} bassboost", style=ButtonStyle.PRIMARY if current == "bassboost" else ButtonStyle.DEFAULT),
            styled_button(text="🚀 Super Bass" + (" ✔️" if current == "superbass" else ""), callback_data=f"dsp_set {chat_id} superbass", style=ButtonStyle.PRIMARY if current == "superbass" else ButtonStyle.DEFAULT),
        ],
        [
            styled_button(text="🌙 Nightcore" + (" ✔️" if current == "nightcore" else ""), callback_data=f"dsp_set {chat_id} nightcore", style=ButtonStyle.PRIMARY if current == "nightcore" else ButtonStyle.DEFAULT),
            styled_button(text="🌧 Slowed+Reverb" + (" ✔️" if current == "slowed" else ""), callback_data=f"dsp_set {chat_id} slowed", style=ButtonStyle.PRIMARY if current == "slowed" else ButtonStyle.DEFAULT),
        ],
        [
            styled_button(text="🎧 8D Audio" + (" ✔️" if current == "8d" else ""), callback_data=f"dsp_set {chat_id} 8d", style=ButtonStyle.PRIMARY if current == "8d" else ButtonStyle.DEFAULT),
            styled_button(text="🌴 Vaporwave" + (" ✔️" if current == "vaporwave" else ""), callback_data=f"dsp_set {chat_id} vaporwave", style=ButtonStyle.PRIMARY if current == "vaporwave" else ButtonStyle.DEFAULT),
        ],
        [
            styled_button(text="✨ Normal / Reset", callback_data=f"dsp_set {chat_id} normal", style=ButtonStyle.DANGER),
            styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DEFAULT),
        ]
    ]
    return types.InlineKeyboardMarkup(buttons)


@app.on_message(filters.command(["eq", "equalizer", "dsp", "effects", "bassboost", "nightcore", "slowed", "8d", "vaporwave", "resetfilter"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def dsp_handler(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    cmd = m.command[0].lower()
    chat_id = m.chat.id

    if cmd in ("eq", "equalizer", "dsp", "effects"):
        curr = await db.get_dsp(chat_id)
        return await m.reply_text(
            f"🎛 <b><u>Real-Time Audio DSP Equalizer & Effects</u></b>\n\nCurrent Effect: <b>{curr.upper()}</b>\n\nSelect an audio effect below to apply instantly:",
            reply_markup=dsp_menu_markup(chat_id, curr),
        )

    effect_map = {
        "bassboost": "bassboost",
        "nightcore": "nightcore",
        "slowed": "slowed",
        "8d": "8d",
        "vaporwave": "vaporwave",
        "resetfilter": "normal",
    }
    chosen = effect_map.get(cmd, "normal")
    await db.set_dsp(chat_id, chosen)

    media = queue.get_current(chat_id)
    if media:
        sent = await m.reply_text(f"🎛 <i>Applying <b>{chosen.upper()}</b> effect to current stream...</i>")
        await anon.play_media(chat_id, sent, media, seek_time=media.time or 1)
        await sent.edit_text(f"✨ <b>Applied {chosen.upper()} effect successfully!</b>")
    else:
        await m.reply_text(f"✨ <b>Audio effect set to {chosen.upper()}.</b>")


@app.on_callback_query(filters.regex(r"^dsp_set") & ~app.bl_users)
@can_manage_vc
async def dsp_callback(_, query: types.CallbackQuery):
    _, chat_id_str, effect = query.data.split()
    chat_id = int(chat_id_str)

    await db.set_dsp(chat_id, effect)
    await query.answer(f"🎛 Applied {effect.upper()} effect!", show_alert=True)

    media = queue.get_current(chat_id)
    if media and await db.get_call(chat_id):
        await anon.play_media(chat_id, query.message, media, seek_time=media.time or 1)

    await query.edit_message_reply_markup(reply_markup=dsp_menu_markup(chat_id, effect))
