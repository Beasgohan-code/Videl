# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Dual-Engine Telegram Bridge (Kurigram/Pyrogram MTProto + Aiogram 3.31+ Bot API 8.x/10.x)

from typing import Optional, Union, Dict, Any, List
import os
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
        ReactionTypeCustomEmoji,
        InputPaidMediaPhoto,
        InputPaidMediaVideo,
        FSInputFile,
        LinkPreviewOptions,
    )
except ImportError:
    AiogramBot = None

# Telegram Animated Message Effect IDs (Bot API 7.x / 8.x / 10.x)
EFFECT_FIRE = "5104841245755180586"         # 🔥 Fire Flame
EFFECT_CELEBRATE = "5046509860389126442"    # 🎉 Celebration Party
EFFECT_HEART = "5107584321108051014"        # ❤️ Heart Burst
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
        """Send message with modern Telegram Visual Message Effect (Bot API 8.x+)."""
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
                logger.debug(f"Aiogram send_with_effect fallback: {ex}")

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
        """Send Telegram Stars payment invoice (Bot API 7.4+ / 8.x+)."""
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

    async def refund_star_payment(self, user_id: int, telegram_payment_charge_id: str) -> bool:
        """Refund a Telegram Stars payment (Bot API 7.4+)."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.refund_star_payment(
                    user_id=user_id,
                    telegram_payment_charge_id=telegram_payment_charge_id,
                )
            except Exception as ex:
                logger.error(f"Telegram Star refund error: {ex}")
        return False

    async def get_star_transactions(self, offset: int = 0, limit: int = 20):
        """Fetch Telegram Stars transactions ledger (Bot API 7.4+)."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.get_star_transactions(offset=offset, limit=limit)
            except Exception as ex:
                logger.error(f"Telegram Star transactions error: {ex}")
        return None

    async def send_paid_media(
        self,
        chat_id: Union[int, str],
        star_count: int,
        media_paths: List[str],
        caption: Optional[str] = None,
    ):
        """Send Paid Media locked behind Telegram Stars (Bot API 7.9+ / 8.x+ / 10.x)."""
        if self.aiogram_bot and InputPaidMediaPhoto:
            try:
                paid_media = []
                for p in media_paths:
                    if p.endswith((".jpg", ".jpeg", ".png", ".webp")):
                        paid_media.append(InputPaidMediaPhoto(media=FSInputFile(p)))
                    elif p.endswith((".mp4", ".mkv", ".mov")):
                        paid_media.append(InputPaidMediaVideo(media=FSInputFile(p)))
                if paid_media:
                    return await self.aiogram_bot.send_paid_media(
                        chat_id=chat_id,
                        star_count=star_count,
                        media=paid_media,
                        caption=caption,
                    )
            except Exception as ex:
                logger.debug(f"Aiogram send_paid_media note: {ex}")
        return None

    async def send_quiz(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        correct_option_id: int,
        explanation: Optional[str] = None,
    ):
        """Send Quiz Poll with explanation (Bot API 8.x+)."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.send_poll(
                    chat_id=chat_id,
                    question=question,
                    options=options,
                    type="quiz",
                    correct_option_id=correct_option_id,
                    explanation=explanation,
                    is_anonymous=False,
                )
            except Exception as ex:
                logger.debug(f"Aiogram send_quiz note: {ex}")

        from videl import app
        try:
            return await app.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                type=types.enums.PollType.QUIZ,
                correct_option_id=correct_option_id,
                explanation=explanation,
                is_anonymous=False,
            )
        except Exception:
            return None

    async def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        allows_multiple_answers: bool = False,
    ):
        """Send standard voting poll."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.send_poll(
                    chat_id=chat_id,
                    question=question,
                    options=options,
                    allows_multiple_answers=allows_multiple_answers,
                    is_anonymous=False,
                )
            except Exception:
                pass

        from videl import app
        try:
            return await app.send_poll(
                chat_id=chat_id,
                question=question,
                options=options,
                allows_multiple_answers=allows_multiple_answers,
                is_anonymous=False,
            )
        except Exception:
            return None

    async def set_bot_profile_photo(self, photo_path: str) -> bool:
        """Set Bot's own profile photo (Bot API 9.4+ / 10.x)."""
        if self.aiogram_bot and hasattr(self.aiogram_bot, "set_my_profile_photo") and os.path.exists(photo_path):
            try:
                return await self.aiogram_bot.set_my_profile_photo(photo=FSInputFile(photo_path))
            except Exception as ex:
                logger.debug(f"Aiogram set_my_profile_photo note: {ex}")
        return False

    async def remove_bot_profile_photo(self) -> bool:
        """Remove Bot's own profile photo (Bot API 9.4+ / 10.x)."""
        if self.aiogram_bot and hasattr(self.aiogram_bot, "remove_my_profile_photo"):
            try:
                return await self.aiogram_bot.remove_my_profile_photo()
            except Exception as ex:
                logger.debug(f"Aiogram remove_my_profile_photo note: {ex}")
        return False

    async def answer_chat_join_request(self, chat_id: Union[int, str], user_id: int) -> bool:
        """Approve a chat join request via Bot API 10.x."""
        if self.aiogram_bot:
            try:
                return await self.aiogram_bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
            except Exception:
                pass
        from videl import app
        try:
            return await app.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
        except Exception:
            return False

    async def send_with_link_preview_options(
        self,
        chat_id: Union[int, str],
        text: str,
        is_disabled: bool = False,
        prefer_small_media: bool = False,
        prefer_large_media: bool = False,
        show_above_text: bool = False,
    ):
        """Send message with Bot API 7.0+ LinkPreviewOptions."""
        if self.aiogram_bot:
            try:
                opts = LinkPreviewOptions(
                    is_disabled=is_disabled,
                    prefer_small_media=prefer_small_media,
                    prefer_large_media=prefer_large_media,
                    show_above_text=show_above_text,
                )
                return await self.aiogram_bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    link_preview_options=opts,
                )
            except Exception:
                pass

        from videl import app
        return await app.send_message(chat_id=chat_id, text=text, disable_web_page_preview=is_disabled)

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
