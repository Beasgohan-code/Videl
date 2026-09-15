# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl - Next-Gen Telegram Voice Chat Music Streamer

from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", 0))
        self.API_HASH = getenv("API_HASH", "")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "")
        self.BOT_NAME = getenv("BOT_NAME", "Videl Music")
        self.MONGO_URL = getenv("MONGO_URL", "")

        self.LOGGER_ID = int(getenv("LOGGER_ID", 0))
        self.OWNER_ID = int(getenv("OWNER_ID", 0))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 30))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 25))

        # Multi-Assistant String Sessions
        self.SESSION1 = getenv("SESSION", getenv("SESSION1", None))
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)
        self.SESSION4 = getenv("SESSION4", None)
        self.SESSION5 = getenv("SESSION5", None)

        # Support & Community Links
        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BeasgohanUpdates")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/BeasgohanSupport")
        self.GITHUB_REPO = getenv("GITHUB_REPO", "https://github.com/Beasgohan-code/Videl")

        # Fallback Video & Music API
        self.API_URL = getenv("API_URL", "https://pvtz.nexgenbots.xyz")
        self.VIDEO_API_URL = getenv("VIDEO_API_URL", "https://api.video.nexgenbots.xyz")
        self.API_KEY = getenv("API_KEY", None)

        # Stream & Automation Flags
        self.AUTO_LEAVE: bool = getenv("AUTO_LEAVE", "False").lower() in ("true", "1", "yes")
        self.AUTO_END: bool = getenv("AUTO_END", "False").lower() in ("true", "1", "yes")
        self.THUMB_GEN: bool = getenv("THUMB_GEN", "True").lower() in ("true", "1", "yes")
        self.VIDEO_PLAY: bool = getenv("VIDEO_PLAY", "True").lower() in ("true", "1", "yes")
        self.CLEANMODE: bool = getenv("CLEANMODE", "True").lower() in ("true", "1", "yes")

        # Localization
        self.LANG_CODE = getenv("LANG_CODE", "en")

        # YouTube Cookie URLs
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "").split(" ")
            if url and ("batbin.me" in url or "pastebin.com" in url or "raw.githubusercontent" in url)
        ]

        # Aesthetic Image Banners
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://telegra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", "https://files.catbox.moe/haagg2.png")
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/zvziwk.jpg")
        self.STATS_IMG = getenv("STATS_IMG", "https://files.catbox.moe/haagg2.png")

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID"]
            if not getattr(self, var)
        ]
        if not (self.SESSION1 or self.SESSION2 or self.SESSION3 or self.SESSION4 or self.SESSION5):
            missing.append("SESSION (or SESSION1)")
            
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
