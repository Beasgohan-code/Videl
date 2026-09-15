# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot API 8.x/10.x Message Effects and Reactions Plugin

from pyrogram import filters, types
from videl import app, bridge
from videl.core.bridge import (
    EFFECT_FIRE,
    EFFECT_CELEBRATE,
    EFFECT_HEART,
    EFFECT_THUMBS_UP,
    EFFECT_STARS,
)
from videl.helpers.button_style import styled_button, ButtonStyle

EFFECT_MAP = {
    "fire": EFFECT_FIRE,
    "flame": EFFECT_FIRE,
    "celebrate": EFFECT_CELEBRATE,
    "party": EFFECT_CELEBRATE,
    "heart": EFFECT_HEART,
    "love": EFFECT_HEART,
    "thumbs": EFFECT_THUMBS_UP,
    "like": EFFECT_THUMBS_UP,
    "stars": EFFECT_STARS,
    "star": EFFECT_STARS,
}


@app.on_message(filters.command(["effect", "fxmsg"]) & ~app.bl_users)
async def effect_command(_, message: types.Message):
    if len(message.command) < 3:
        effects_list = ", ".join([f"<code>{k}</code>" for k in ["fire", "celebrate", "heart", "thumbs", "stars"]])
        return await message.reply_text(
            f"✨ <b><u>Bot API Visual Message Effects</u></b>\n\n"
            f"<b>Usage:</b> <code>/effect [effect_name] [your message text]</code>\n"
            f"<b>Available Effects:</b> {effects_list}\n\n"
            f"<i>Example:</i> <code>/effect fire Now blasting your favorite track! 🔥</code>",
            quote=True,
        )

    effect_type = message.command[1].lower()
    effect_id = EFFECT_MAP.get(effect_type)
    if not effect_id:
        return await message.reply_text(f"❌ Unknown effect '{effect_type}'. Choose from fire, celebrate, heart, thumbs, stars.", quote=True)

    text_to_send = message.text.split(None, 2)[2]

    # Send using Bot API 8.x/10.x bridge
    sent = await bridge.send_message_with_effect(
        chat_id=message.chat.id,
        text=text_to_send,
        effect_id=effect_id,
        reply_to_message_id=message.id,
    )

    if not sent:
        # Fallback normal send
        await message.reply_text(text_to_send, quote=True)


@app.on_message(filters.command(["react", "reaction"]) & ~app.bl_users)
async def react_command(_, message: types.Message):
    target_msg = message.reply_to_message or message
    emoji = "🔥"
    if len(message.command) > 1:
        emoji = message.command[1]

    ok = await bridge.set_message_reaction(
        chat_id=message.chat.id,
        message_id=target_msg.id,
        reaction_emoji=emoji,
    )
    if not ok:
        try:
            await app.send_reaction(chat_id=message.chat.id, message_id=target_msg.id, emoji=emoji)
        except Exception:
            pass
