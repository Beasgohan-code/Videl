"""Minimal async Bot API client; transport is injectable for tests and adapters."""
from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.request import Request, urlopen

from .rich_message import RichMessage

Transport = Callable[[str, dict[str, Any]], Awaitable[dict[str, Any]]]


async def _urllib_transport(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Dependency-free fallback transport (use aiohttp in production if desired)."""
    import asyncio
    body = json.dumps(payload).encode()
    request = Request(url, data=body, headers={"Content-Type": "application/json"})
    response = await asyncio.to_thread(urlopen, request, timeout=30)
    return json.loads(response.read())


class Bot:
    def __init__(self, token: str, *, transport: Transport | None = None) -> None:
        if not token.strip():
            raise ValueError("bot token cannot be empty")
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.transport = transport or _urllib_transport

    async def request(self, method: str, **payload: Any) -> dict[str, Any]:
        result = await self.transport(f"{self.base_url}/{method}", payload)
        if not result.get("ok", False):
            raise RuntimeError(result.get("description", "Telegram API request failed"))
        return result["result"]

    async def send_message(self, chat_id: int | str, message: str | RichMessage,
                           **kwargs: Any) -> dict[str, Any]:
        payload = message.to_payload(chat_id) if isinstance(message, RichMessage) else {
            "chat_id": chat_id, "text": message, **kwargs
        }
        if isinstance(message, RichMessage):
            payload.update(kwargs)
        return await self.request("sendMessage", **payload)

    async def edit_message(self, chat_id: int | str, message_id: int,
                           message: str | RichMessage, **kwargs: Any) -> dict[str, Any]:
        payload = message.to_payload(chat_id) if isinstance(message, RichMessage) else {
            "chat_id": chat_id, "message_id": message_id, "text": message, **kwargs
        }
        payload["message_id"] = message_id
        if isinstance(message, RichMessage):
            payload.update(kwargs)
        return await self.request("editMessageText", **payload)

    async def delete_message(self, chat_id: int | str, message_id: int) -> bool:
        return bool(await self.request("deleteMessage", chat_id=chat_id, message_id=message_id))
