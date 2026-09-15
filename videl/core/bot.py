# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot Core Client

import pyrogram
from pyrogram import enums, types
from videl import config, logger
from videl.helpers.rich_message import RichMessage


class Bot(pyrogram.Client):
    def __init__(self):
        client_kwargs = {
            "name": "VidelBot",
            "api_id": config.API_ID if config.API_ID else 1,
            "api_hash": config.API_HASH if config.API_HASH else "dummy_api_hash_12345",
            "bot_token": config.BOT_TOKEN if config.BOT_TOKEN else "123456:dummy_bot_token",
            "parse_mode": enums.ParseMode.HTML,
            "max_concurrent_transmissions": 8,
        }
        if hasattr(types, "LinkPreviewOptions"):
            client_kwargs["link_preview_options"] = types.LinkPreviewOptions(is_disabled=True)

        super().__init__(**client_kwargs)
        self.owner = config.OWNER_ID
        self.logger_id = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)
        self.name = config.BOT_NAME

    async def boot(self):
        """Starts the bot client and validates logger permissions."""
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(self.logger_id, f"✨ <b>{self.name}</b> has been started successfully!")
            member = await self.get_chat_member(self.logger_id, self.id)
            if member.status != enums.ChatMemberStatus.ADMINISTRATOR:
                logger.warning("Please ensure the bot is an ADMINISTRATOR in the logger group.")
        except Exception as ex:
            logger.warning(f"Could not verify logger channel/group ({self.logger_id}): {ex}")

        logger.info(f"Videl Bot started as @{self.username} (ID: {self.id})")

    async def send_rich(
        self,
        chat_id: int | str,
        rich_msg: RichMessage | str,
        reply_markup=None,
        reply_to_message_id: int = None,
    ) -> types.Message:
        """Send rich message with structured blocks or HTML markup."""
        text = rich_msg.render_html() if isinstance(rich_msg, RichMessage) else rich_msg
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
        )

    async def exit(self):
        try:
            await self.send_message(self.logger_id, f"🛑 <b>{self.name}</b> is shutting down...")
        except Exception:
            pass
        await super().stop()
        logger.info("Videl Bot client stopped.")
