# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl YouTube & Streaming Resolver

import asyncio
import os
import random
import re
from pathlib import Path
from typing import List, Optional
import aiohttp
import yt_dlp

try:
    from py_yt import VideosSearch, Playlist
except ImportError:
    from py_yt_search import VideosSearch, Playlist

from videl import config, logger
from videl.helpers._api import NexGenApi
from videl.helpers._dataclass import Track
from videl.helpers._utilities import to_seconds


class YouTube:
    def __init__(self):
        self.api = None
        self.base = "https://www.youtube.com/watch?v="
        self.cookies: List[str] = []
        self.checked = False
        self.cookie_dir = "cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )
        self.iregex = re.compile(
            r"https?://(?:www\.|m\.|music\.)?(?:youtube\.com|youtu\.be)"
            r"(?!/(watch\?v=[A-Za-z0-9_-]{11}|shorts/[A-Za-z0-9_-]{11}"
            r"|playlist\?list=PL[A-Za-z0-9_-]+|[A-Za-z0-9_-]{11}))\S*"
        )
        # Spotify / Apple Music regex
        self.spotify_regex = re.compile(r"https?://open\.spotify\.com/(track|album|playlist)/[a-zA-Z0-9]+")
        self.apple_music_regex = re.compile(r"https?://music\.apple\.com/[a-zA-Z0-9/_-]+")

        if config.API_URL and config.VIDEO_API_URL and config.API_KEY:
            self.api = NexGenApi(config.API_URL, config.API_KEY, config.VIDEO_API_URL)

    def get_cookies(self) -> Optional[str]:
        if not self.checked:
            if os.path.exists(self.cookie_dir):
                for file in os.listdir(self.cookie_dir):
                    if file.endswith(".txt"):
                        self.cookies.append(os.path.join(self.cookie_dir, file))
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("No YouTube cookies found. Using default public streaming.")
            return None
        return random.choice(self.cookies)

    async def save_cookies(self, urls: List[str]) -> None:
        logger.info("Saving cookies from URLs...")
        async with aiohttp.ClientSession() as session:
            for url in urls:
                name = url.split("/")[-1]
                link = "https://batbin.me/raw/" + name if "batbin.me" in url else url
                try:
                    async with session.get(link) as resp:
                        resp.raise_for_status()
                        with open(os.path.join(self.cookie_dir, f"{name}.txt"), "wb") as fw:
                            fw.write(await resp.read())
                except Exception as e:
                    logger.warning(f"Failed to fetch cookie {url}: {e}")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    def invalid(self, url: str) -> bool:
        return bool(re.match(self.iregex, url))

    def is_spotify(self, url: str) -> bool:
        return bool(re.match(self.spotify_regex, url))

    def is_apple_music(self, url: str) -> bool:
        return bool(re.match(self.apple_music_regex, url))

    async def search(self, query: str, message_id: int, video: bool = False) -> Optional[Track]:
        try:
            search_obj = VideosSearch(query, limit=1, with_live=False)
            results = await search_obj.next()
            if results and results.get("result"):
                data = results["result"][0]
                return Track(
                    id=data.get("id", ""),
                    channel_name=data.get("channel", {}).get("name", "Unknown Artist"),
                    duration=data.get("duration", "00:00"),
                    duration_sec=to_seconds(data.get("duration", "00:00")),
                    message_id=message_id,
                    title=data.get("title", "Unknown Title")[:50],
                    thumbnail=data.get("thumbnails", [{}])[-1].get("url", "").split("?")[0],
                    url=data.get("link", f"https://youtube.com/watch?v={data.get('id')}"),
                    view_count=data.get("viewCount", {}).get("short", "0 views"),
                    video=video,
                )
        except Exception as ex:
            logger.error(f"YouTube search error for query '{query}': {ex}")
        return None

    async def playlist(self, limit: int, user: str, url: str, video: bool) -> List[Track]:
        tracks: List[Track] = []
        try:
            plist = await Playlist.get(url)
            videos = plist.get("videos", [])
            for data in videos[:limit]:
                track = Track(
                    id=data.get("id", ""),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=data.get("duration", "00:00"),
                    duration_sec=to_seconds(data.get("duration", "00:00")),
                    title=data.get("title", "Unknown")[:50],
                    thumbnail=data.get("thumbnails", [{}])[-1].get("url", "").split("?")[0],
                    url=data.get("link", "").split("&list=")[0],
                    user=user,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except Exception as ex:
            logger.error(f"Error fetching YouTube playlist: {ex}")
        return tracks

    async def download(self, video_id: str, video: bool = False) -> Optional[str]:
        if self.api:
            if file_path := await self.api.download(video_id, video):
                return file_path

        url = self.base + video_id
        ext = "mp4" if video else "webm"
        filename = f"downloads/{video_id}.{ext}"

        if Path(filename).exists():
            return filename

        cookie = self.get_cookies()
        base_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "geo_bypass": True,
            "no_warnings": True,
            "overwrites": False,
            "nocheckcertificate": True,
            "cookiefile": cookie,
        }

        if video:
            ydl_opts = {
                **base_opts,
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio)",
                "merge_output_format": "mp4",
            }
        else:
            ydl_opts = {
                **base_opts,
                "format": "bestaudio[ext=webm][acodec=opus]/bestaudio/best",
            }

        def _download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except Exception as ex:
                    logger.warning(f"yt-dlp download failed for {url}: {ex}")
                    return None
            return filename

        return await asyncio.to_thread(_download)
