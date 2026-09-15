"""A composable rich message that maps cleanly to Telegram send methods."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .buttons import Keyboard


@dataclass(slots=True)
class RichMessage:
    text: str
    parse_mode: str = "HTML"
    keyboard: Keyboard | None = None
    disable_web_page_preview: bool = True
    protect_content: bool = False
    disable_notification: bool = False
    message_thread_id: int | None = None
    reply_to_message_id: int | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("message text cannot be empty")

    def buttons(self, keyboard: Keyboard) -> "RichMessage":
        self.keyboard = keyboard
        return self

    def option(self, name: str, value: Any) -> "RichMessage":
        self.extra[name] = value
        return self

    def to_payload(self, chat_id: int | str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": self.text,
            "parse_mode": self.parse_mode,
            "disable_web_page_preview": self.disable_web_page_preview,
            "protect_content": self.protect_content,
            "disable_notification": self.disable_notification,
        }
        if self.keyboard is not None:
            payload["reply_markup"] = self.keyboard.to_dict()
        if self.message_thread_id is not None:
            payload["message_thread_id"] = self.message_thread_id
        if self.reply_to_message_id is not None:
            payload["reply_parameters"] = {"message_id": self.reply_to_message_id}
        payload.update(self.extra)
        return payload

    def __str__(self) -> str:
        return self.text
