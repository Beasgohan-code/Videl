# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl - Next-Gen Telegram Voice Chat Music Streamer

import asyncio
import logging
import time
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("motor").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

logger = logging.getLogger("Videl")
__version__ = "3.5.0"

from config import Config

config = Config()
tasks = []
boot = time.time()

from videl.core.dir import ensure_dirs
ensure_dirs()

from videl.core.lang import Language
lang = Language()

from videl.core.mongo import MongoDB
db = MongoDB()

from videl.core.bot import Bot
app = Bot()

from videl.core.userbot import Userbot
userbot = Userbot()

from videl.core.telegram import Telegram
from videl.core.youtube import YouTube
tg = Telegram()
yt = YouTube()

from videl.helpers._queue import Queue
from videl.helpers._thumbnails import Thumbnail
queue = Queue()
thumb = Thumbnail()

from videl.core.calls import TgCall
anon = TgCall()


async def stop() -> None:
    logger.info("Stopping Videl services...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    await app.exit()
    await userbot.exit()
    await db.close()
    await thumb.close()
    if yt.api and yt.api.session:
        await yt.api.session.close()

    logger.info("Videl stopped gracefully.\n")
