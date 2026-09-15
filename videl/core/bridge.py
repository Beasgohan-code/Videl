# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Dual-Engine Telegram Bridge (Kurigram/Pyrogram MTProto + Aiogram 3.x Bot API)

from typing import Optional, Union, Dict, Any, List
from videl import config, logger
from videl.helpers.rich_message import RichMessage

try:
    from aiogram import Bot as AiogramBot
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode
    from aiogram.types import (
        InlineKeyboardMarkup as AioInlineKeyboardMarkup,
        InlineKeyboardButton as AioInlineKeyboardButton,
        LabeledPrice,
        ReactionTypeEmoji,
    )
except ImportError:
    AiogramBot = None

# Popular Telegram Message Effect IDs (Bot API 7.x / 8.x+)
EFFECT_FIRE = "5104841245755180586"         # 🔥 Fire Effect
EFFECT_CELEBRATE = "5046509860389126442"    # 🎉 Celebration Party
EFFECT_HEART = "5107584321108051014"        # ❤️ Heart Explosion
EFFECT_THUMBS_UP = "5107584321108051014"   # 👍 Thumbs Up
EFFECT_LIGHTNING = "5104858069142078462"    # ⚡ Lightning Flare
EFFECT_STARS = "5046509860389126442"        # ⭐️ Stars / Confetti


class TelegramBridge:
    def __init__(self):
        self.aiogram_bot: Optional[AiogramBot] = None
        if AiogramBot and config.BOT_TOKEN:
            try:
                self.aiogram_bot = AiogramBot(
                    token=config.BOT_TOKEN,
                    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                )
            except Exception as e:
                logger.debug(f"Aiogram bridge init note: {e}")

    async def close(self):
        if self.aiogram_bot and self.aiogram_bot.session:
            try:
                await self.aiogram_bot.session.close()
            except Exception:
                pass

    async def send_with_effect(
        self,
        chat_id: Union[int, str],
        text: str,
        effect_id: str = EFFECT_FIRE,
        reply_markup=None,
        reply_to_message_id: Optional[int] = None,
    ):
        """Send message with Telegram Visual Message Effect (e.g. Fire, Party, Heart)."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    message_effect_id=effect_id,
                    reply_markup=reply_markup,
                    reply_to_message_id=reply_to_message_id,
                )
            except Exception as ex:
                logger.debug(f"Aiogram send_with_effect fallback to pyrogram: {ex}")

        from videl import app
        return await app.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, reply_to_message_id=reply_to_message_id)

    async def send_message_with_effect(
        self,
        chat_id: Union[int, str],
        text: str,
        effect_id: str = EFFECT_FIRE,
        reply_markup=None,
        reply_to_message_id: Optional[int] = None,
    ):
        return await self.send_with_effect(
            chat_id=chat_id,
            text=text,
            effect_id=effect_id,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    async def set_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        emoji: str = "🔥",
    ) -> bool:
        """Set message reaction via Bot API 8.x+."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.set_message_reaction(
                    chat_id=chat_id,
                    message_id=message_id,
                    reaction=[ReactionTypeEmoji(emoji=emoji)],
                )
            except Exception:
                pass
        return False

    async def set_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        reaction_emoji: str = "🔥",
    ) -> bool:
        return await self.set_reaction(chat_id=chat_id, message_id=message_id, emoji=reaction_emoji)


    async def send_star_invoice(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        stars_amount: int = 25,
    ):
        """Send Telegram Stars payment invoice (Bot API 7.4+)."""
        if self.aiogram_bot:
            try:
                prices = [LabeledPrice(label="Star Support", amount=stars_amount)]
                return await self.aiogram_bot.send_invoice(
                    chat_id=chat_id,
                    title=title,
                    description=description,
                    payload=payload,
                    currency="XTR",  # Telegram Stars Currency Code
                    prices=prices,
                )
            except Exception as ex:
                logger.error(f"Telegram Stars invoice error: {ex}")
        return None

    async def send_rich(
        self,
        chat_id: Union[int, str],
        rich_msg: Union[RichMessage, str],
        reply_markup=None,
    ):
        """Send rich structured block message."""
        text = rich_msg.render_html() if isinstance(rich_msg, RichMessage) else rich_msg
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=reply_markup,
                )
            except Exception:
                pass

        from videl import app
        return await app.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


bridge = TelegramBridge()
