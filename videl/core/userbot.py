# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Multi-Assistant Userbot Core

from pyrogram import Client
from videl import config, logger


class Userbot:
    def __init__(self):
        self.clients = []
        sessions = {
            1: config.SESSION1,
            2: config.SESSION2,
            3: config.SESSION3,
            4: config.SESSION4,
            5: config.SESSION5,
        }
        for num, session in sessions.items():
            if session:
                client = Client(
                    name=f"VidelUB{num}",
                    api_id=config.API_ID if config.API_ID else 1,
                    api_hash=config.API_HASH if config.API_HASH else "dummy_api_hash_12345",
                    session_string=session,
                    no_updates=True,
                )
                setattr(self, f"ub_{num}", client)

    async def boot_client(self, num: int, client: Client):
        try:
            await client.start()
            client.id = client.me.id
            client.name = client.me.first_name
            client.username = client.me.username
            client.mention = client.me.mention
            self.clients.append(client)

            try:
                await client.send_message(config.LOGGER_ID, f"⚡ Assistant {num} (ID: {client.id}) started.")
            except Exception:
                pass

            logger.info(f"Assistant {num} booted as @{client.username} ({client.id})")
        except Exception as ex:
            logger.error(f"Failed to boot Assistant {num}: {ex}")

    async def boot(self):
        for num in range(1, 6):
            if hasattr(self, f"ub_{num}"):
                await self.boot_client(num, getattr(self, f"ub_{num}"))
        if not self.clients:
            logger.warning("No assistant sessions provided. Streaming requires at least 1 assistant session.")

    async def exit(self):
        for idx, client in enumerate(self.clients, 1):
            try:
                await client.stop()
            except Exception:
                pass
        logger.info("All assistant clients stopped.")
