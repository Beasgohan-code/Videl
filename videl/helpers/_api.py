# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Streaming API Client

import aiohttp
from typing import Optional
from videl import logger


class NexGenApi:
    def __init__(self, api_url: str, api_key: str, video_api_url: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.video_api_url = video_api_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.api_key}"})
        return self.session

    async def download(self, video_id: str, video: bool = False) -> Optional[str]:
        base = self.video_api_url if video else self.api_url
        endpoint = f"{base}/download/{video_id}"
        session = await self.get_session()
        try:
            async with session.get(endpoint) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("file_path") or data.get("url")
        except Exception as ex:
            logger.debug(f"API download fallback error: {ex}")
        return None
