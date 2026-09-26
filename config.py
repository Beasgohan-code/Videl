"""
config.py — All environment variables in one place.
Copy sample.env → .env and fill in your values.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _req(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        print(f"❌ Missing required env: {name}", file=sys.stderr)
        sys.exit(1)
    return val


# ── Required ──────────────────────────────────────────────────────────────────
try:
    API_ID = int(_req("API_ID"))
except ValueError:
    print("❌ API_ID must be a number", file=sys.stderr)
    sys.exit(1)

API_HASH = _req("API_HASH")
BOT_TOKEN = _req("BOT_TOKEN")
_raw_session = _req("STRING_SESSION").strip().strip('"').strip("'")
# Fix common paste issues: whitespace / missing base64 padding
_raw_session = "".join(_raw_session.split())
if len(_raw_session) % 4:
    _raw_session += "=" * (4 - len(_raw_session) % 4)
STRING_SESSION = _raw_session
MONGO_DB_URL = _req("MONGO_DB_URL")

try:
    OWNER_ID = int(_req("OWNER_ID"))
except ValueError:
    print("❌ OWNER_ID must be a number", file=sys.stderr)
    sys.exit(1)

# ── Optional ──────────────────────────────────────────────────────────────────
BOT_NAME = os.getenv("BOT_NAME", "Videl Music")
BOT_LINK = os.getenv("BOT_LINK", "https://t.me/VidelMusicBot")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "https://t.me/BeasgohanUpdates")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/BeasgohanSupport")
LOGGER_ID = int(os.getenv("LOGGER_ID", "0") or "0")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://files.catbox.moe/ddzvc0.jpg")
SESSION_NAME = os.getenv("SESSION_NAME", "videl")
# Render / Railway / Koyeb inject PORT — always prefer it
PORT = int(os.getenv("PORT", "10000"))

START_PHOTOS = [
    p.strip()
    for p in os.getenv("START_PHOTOS", "https://files.catbox.moe/jgt2vm.png").split(",")
    if p.strip()
] or ["https://files.catbox.moe/jgt2vm.png"]

MAX_DURATION_SECONDS = int(os.getenv("MAX_DURATION_SECONDS", "1800"))
QUEUE_LIMIT = int(os.getenv("QUEUE_LIMIT", "20"))
COOLDOWN = int(os.getenv("COOLDOWN", "10"))
