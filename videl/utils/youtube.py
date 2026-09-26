# --------------------------------------------------------------------------------
#  Videl © 2026 | Developed by Beasgohan-code
#  Fork & improve freely under MIT. Keep credits.
# --------------------------------------------------------------------------------

import asyncio
import logging
import os
import re
from typing import Union

import aiofiles
import aiohttp
import yt_dlp
from py_yt import Playlist, VideosSearch
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

from videl.utils.formatters import sec_to_iso

logger = logging.getLogger(__name__)

# ── API config ────────────────────────────────────────────────────────────────
SHRUTI_API_URL        = os.environ.get("SHRUTI_API_URL", "https://api.shrutibots.site")
SHRUTI_API_KEY        = os.environ.get("SHRUTI_API_KEY", "ShrutiBots1JyNWUFBwhFiouHmUyXC")  # Get from @SHRUTIAPIBOT on Telegram
DOWNLOAD_DIR          = "downloads"
SHRUTI_TOKEN_TIMEOUT  = 10    # seconds — fetch download token
SHRUTI_STREAM_TIMEOUT = 900   # 15 min  — stream long songs

_file_cache: dict[str, str] = {}


# ═════════════════════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _extract_video_id(url: str) -> str:
    """Extract raw video ID from any YouTube URL format."""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return url


def _cleanup(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def time_to_seconds(time) -> int:
    """Convert M:SS or H:MM:SS string to total seconds."""
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# ═════════════════════════════════════════════════════════════════════════════
# CLASSIC yt-dlp DOWNLOAD (old reliable)
# ═════════════════════════════════════════════════════════════════════════════

def _yt_url(link: str) -> str:
    vid = _extract_video_id(link)
    if not vid:
        return link
    if "youtube.com" in str(link) or "youtu.be" in str(link):
        return link
    return f"https://www.youtube.com/watch?v={vid}"


def _find_file(video_id: str) -> str | None:
    """Find any downloaded file for this video id."""
    if not video_id or not os.path.isdir(DOWNLOAD_DIR):
        return None
    try:
        for name in os.listdir(DOWNLOAD_DIR):
            if name.startswith(video_id + ".") or name.startswith(video_id + "-"):
                path = os.path.join(DOWNLOAD_DIR, name)
                if os.path.isfile(path) and os.path.getsize(path) > 1024:
                    return path
    except Exception:
        pass
    return None


def _sync_ytdlp(url: str, video: bool = False) -> str | None:
    """
    Classic synchronous yt-dlp download — the old reliable way.
    Returns local file path or None.
    """
    video_id = _extract_video_id(url)
    if not video_id or len(video_id) < 3:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    found = _find_file(video_id)
    if found:
        return found

    outtmpl = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
    watch = _yt_url(url)

    # Optional cookies (age-gate / datacenter IP blocks)
    cookiefile = os.environ.get("YTDLP_COOKIES") or os.environ.get("COOKIES_PATH")

    if video:
        fmt = "best[height<=720]/bestvideo[height<=720]+bestaudio/best"
    else:
        # m4a preferred — no ffmpeg convert needed for PyTgCalls
        fmt = "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best"

    base = {
        "format": fmt,
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "noplaylist": True,
        "retries": 5,
        "fragment_retries": 5,
        "file_access_retries": 3,
        "ignoreerrors": False,
        "overwrites": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
            ),
        },
    }
    if cookiefile and os.path.isfile(cookiefile):
        base["cookiefile"] = cookiefile

    # Multiple YouTube player clients (order matters)
    clients = [
        ["android", "android_music"],
        ["ios", "ios_music"],
        ["mweb"],
        ["tv", "tv_embedded"],
        ["web"],
    ]

    last_err = None
    for i, client in enumerate(clients, 1):
        o = {
            **base,
            "extractor_args": {"youtube": {"player_client": client}},
        }
        try:
            with yt_dlp.YoutubeDL(o) as ydl:
                info = ydl.extract_info(watch, download=True)
                if not info:
                    continue
                path = None
                reqs = info.get("requested_downloads") or []
                if reqs:
                    path = reqs[0].get("filepath")
                if not path:
                    path = ydl.prepare_filename(info)
                # postprocessors may change extension
                if path and not os.path.exists(path):
                    stem = os.path.splitext(path)[0]
                    for ext in (".m4a", ".webm", ".opus", ".mp3", ".mp4", ".mkv", ".ogg"):
                        if os.path.exists(stem + ext):
                            path = stem + ext
                            break
                if path and os.path.exists(path) and os.path.getsize(path) > 1024:
                    logger.info(
                        f"[yt-dlp] OK client={client} "
                        f"{os.path.getsize(path)//1024}KB → {path}"
                    )
                    return path
                found = _find_file(video_id)
                if found:
                    return found
        except Exception as e:
            last_err = e
            logger.warning(f"[yt-dlp] client={client} failed: {e}")

    # CLI fallback (system / pip entrypoint)
    try:
        import subprocess
        import shutil

        bin_path = shutil.which("yt-dlp") or "yt-dlp"
        cmd = [
            bin_path,
            "-f", fmt,
            "-o", outtmpl,
            "--no-playlist",
            "--geo-bypass",
            "--no-check-certificates",
            "--extractor-args", "youtube:player_client=android,ios,mweb",
            "-q",
            watch,
        ]
        if cookiefile and os.path.isfile(cookiefile):
            cmd[1:1] = ["--cookies", cookiefile]
        subprocess.run(cmd, check=False, timeout=240, capture_output=True)
        found = _find_file(video_id)
        if found:
            logger.info(f"[yt-dlp-cli] OK {found}")
            return found
    except Exception as e:
        logger.warning(f"[yt-dlp-cli] {e}")
        last_err = last_err or e

    if last_err:
        logger.error(f"[yt-dlp] final error: {last_err}")
    return None


async def download_song(link: str) -> str:
    """Classic audio download via yt-dlp."""
    video_id = _extract_video_id(link)
    if not video_id:
        return None
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    cached = _find_file(video_id)
    if cached:
        return cached
    try:
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: _sync_ytdlp(link, video=False)
        )
    except Exception as e:
        logger.error(f"[download_song] {e}")
        return None


async def download_video(link: str) -> str:
    """Classic video download via yt-dlp."""
    video_id = _extract_video_id(link)
    if not video_id:
        return None
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    cached = _find_file(video_id)
    if cached:
        return cached
    try:
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: _sync_ytdlp(link, video=True)
        )
    except Exception as e:
        logger.error(f"[download_video] {e}")
        return None


async def resolve_stream(url: str, video: bool = False) -> str:
    """
    Local file / cache / classic yt-dlp.
    """
    if url and os.path.exists(url) and os.path.isfile(url):
        return url

    if url in _file_cache and os.path.exists(_file_cache[url]):
        return _file_cache[url]

    video_id = _extract_video_id(url)
    cached = _find_file(video_id)
    if cached:
        _file_cache[url] = cached
        return cached

    logger.info(f"[resolve] downloading {video_id} video={video}")
    path = await (download_video(url) if video else download_song(url))
    if path and os.path.exists(path):
        _file_cache[url] = path
        return path

    # One more direct sync attempt with real error
    err = None
    try:
        path = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _sync_ytdlp(url, video=video)
        )
        if path:
            _file_cache[url] = path
            return path
    except Exception as e:
        err = e
        logger.error(f"[resolve] {e}")

    raise Exception(str(err) if err else f"yt-dlp could not download {video_id}")


# ═════════════════════════════════════════════════════════════════════════════
# PUBLIC — YOUTUBE SEARCH / METADATA
# ═════════════════════════════════════════════════════════════════════════════

async def search_yt(query: str):
    """Search YouTube for a video or playlist. Returns metadata tuple or playlist dict."""

    # ── Playlist ──────────────────────────────────────────────────────────────
    if "playlist?list=" in query or "&list=" in query:
        pl   = await Playlist.get(query)
        vids = pl.get("videos") or []
        if not vids:
            raise Exception("ᴩʟᴀʏʟɪsᴛ ɪs ᴇᴍᴩᴛʏ")

        items = []
        for v in vids:
            raw = v.get("duration", {})
            if isinstance(raw, dict):
                try:
                    secs = int(raw.get("secondsText", 0))
                except Exception:
                    secs = 0
            else:
                try:
                    secs = int(raw)
                except Exception:
                    secs = 0

            thumbs = v.get("thumbnails") or []
            thumb  = thumbs[0].get("url", "").split("?")[0] if thumbs else ""
            items.append({
                "link":      f"https://www.youtube.com/watch?v={v['id']}",
                "title":     v.get("title", "Unknown"),
                "duration":  sec_to_iso(secs),
                "thumbnail": thumb,
            })
        return {"playlist": items}

    # ── Single video search (first result — backward compatible) ──────────────
    items = await search_yt_multi(query, limit=1)
    if not items:
        raise Exception("ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ")
    r = items[0]
    return (r["url"], r["title"], r["duration_iso"], r["thumbnail"])


async def search_yt_multi(query: str, limit: int = 5) -> list:
    """
    Search YouTube and return up to `limit` results.
    Each item: {url, title, duration, duration_iso, thumbnail, channel}
    """
    if "playlist?list=" in query or "&list=" in query:
        # keep playlist behaviour in search_yt
        return []

    search = VideosSearch(query, limit=min(max(limit, 1), 10))
    results = await search.next()
    lst = results.get("result", [])
    if not lst:
        return []

    out = []
    for r in lst:
        url = r.get("link") or f"https://www.youtube.com/watch?v={r['id']}"
        title = r.get("title", "Unknown")
        vid = r.get("id") or ""
        # Prefer stable ytimg CDN (avoids broken/expired search-result thumbs)
        thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg" if vid else ""
        if not thumb:
            raw = (r.get("thumbnails") or [{}])[0].get("url", "")
            thumb = raw.split("?")[0] if raw else ""
        dur = r.get("duration") or "0:00"
        channel = ""
        try:
            channel = (r.get("channel") or {}).get("name", "") or r.get("channelName", "")
        except Exception:
            pass

        parts = [int(x) for x in dur.split(":") if x.isdigit() or x]
        try:
            parts = [int(x) for x in dur.split(":")]
            secs = (
                parts[0] * 3600 + parts[1] * 60 + parts[2]
                if len(parts) == 3
                else (parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0])
            )
        except Exception:
            secs = 0

        out.append({
            "url": url,
            "title": title,
            "duration": dur,
            "duration_iso": sec_to_iso(secs),
            "thumbnail": thumb,
            "channel": channel,
            "video_id": r.get("id", ""),
        })
    return out


# ═════════════════════════════════════════════════════════════════════════════
# PUBLIC — YouTubeAPI CLASS (full-featured, from Youtube5 style)
# ═════════════════════════════════════════════════════════════════════════════

class YouTubeAPI:
    def __init__(self):
        self.base     = "https://www.youtube.com/watch?v="
        self.regex    = r"(?:youtube\.com|youtu\.be)"
        self.status   = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg      = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _build_link(self, link: str, videoid) -> str:
        return (self.base + link) if videoid else link

    def _strip_extra(self, link: str) -> str:
        return link.split("&")[0] if "&" in link else link

    # ── Public methods ────────────────────────────────────────────────────────

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset: entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        link = self._strip_extra(self._build_link(link, videoid))
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title        = result["title"]
            duration_min = result["duration"]
            thumbnail    = result["thumbnails"][0]["url"].split("?")[0]
            vidid        = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None) -> str:
        link = self._strip_extra(self._build_link(link, videoid))
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None) -> str:
        link = self._strip_extra(self._build_link(link, videoid))
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None) -> str:
        link = self._strip_extra(self._build_link(link, videoid))
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        link = self._strip_extra(self._build_link(link, videoid))
        try:
            downloaded_file = await download_video(link)
            if downloaded_file:
                return 1, downloaded_file
            return 0, "Video download failed"
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(
        self, link: str, limit: int, user_id, videoid: Union[bool, str] = None
    ) -> list:
        if videoid:
            link = self.listbase + link
        link = self._strip_extra(link)
        try:
            plist = await Playlist.get(link)
        except Exception:
            return []
        videos = plist.get("videos") or []
        ids = []
        for data in videos[:limit]:
            if not data:
                continue
            vid = data.get("id")
            if not vid:
                continue
            ids.append(vid)
        return ids

    async def track(self, link: str, videoid: Union[bool, str] = None):
        link = self._strip_extra(self._build_link(link, videoid))
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title        = result["title"]
            duration_min = result["duration"]
            vidid        = result["id"]
            yturl        = result["link"]
            thumbnail    = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title":        title,
            "link":         yturl,
            "vidid":        vidid,
            "duration_min": duration_min,
            "thumb":        thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        link = self._strip_extra(self._build_link(link, videoid))
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for fmt in r["formats"]:
                try:
                    if "dash" not in str(fmt["format"]).lower():
                        formats_available.append(
                            {
                                "format":      fmt["format"],
                                "filesize":    fmt.get("filesize"),
                                "format_id":   fmt["format_id"],
                                "ext":         fmt["ext"],
                                "format_note": fmt["format_note"],
                                "yturl":       link,
                            }
                        )
                except Exception:
                    continue
        return formats_available, link

    async def slider(
        self, link: str, query_type: int, videoid: Union[bool, str] = None
    ):
        link = self._strip_extra(self._build_link(link, videoid))
        a      = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title        = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid        = result[query_type]["id"]
        thumbnail    = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video:     Union[bool, str] = None,
        videoid:   Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title:     Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        try:
            if video or songvideo:
                downloaded_file = await download_video(link)
            else:
                downloaded_file = await download_song(link)
            if downloaded_file:
                return downloaded_file, True
            return None, False
        except Exception:
            return None, False
