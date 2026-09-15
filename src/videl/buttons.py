"""Button and keyboard primitives for Telegram Bot API payloads."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ButtonStyle(str, Enum):
    """Semantic styles understood by Videl's renderer.

    Telegram clients do not currently guarantee custom button colours, so style is
    omitted from Bot API payloads by default and remains available to adapters.
    """
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    LINK = "link"


@dataclass(frozen=True, slots=True)
class Button:
    text: str
    callback_data: str | None = None
    url: str | None = None
    web_app: Mapping[str, Any] | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    login_url: Mapping[str, Any] | None = None
    style: ButtonStyle | str | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("button text cannot be empty")
        targets = [self.callback_data, self.url, self.web_app, self.switch_inline_query,
                   self.switch_inline_query_current_chat, self.login_url]
        if sum(value is not None for value in targets) > 1:
            raise ValueError("a button may have only one action")
        if self.callback_data is not None and len(self.callback_data.encode()) > 64:
            raise ValueError("callback_data must be at most 64 bytes")

    def to_dict(self, *, include_style: bool = False) -> dict[str, Any]:
        data: dict[str, Any] = {"text": self.text}
        for key in ("callback_data", "url", "web_app", "switch_inline_query",
                    "switch_inline_query_current_chat", "login_url"):
            value = getattr(self, key)
            if value is not None:
                data[key] = dict(value) if isinstance(value, Mapping) else value
        if include_style and self.style is not None:
            data["style"] = self.style.value if isinstance(self.style, ButtonStyle) else self.style
        return data


@dataclass(slots=True)
class Keyboard:
    rows: list[list[Button]] = field(default_factory=list)
    inline: bool = True
    resize_keyboard: bool = True
    one_time_keyboard: bool = False
    selective: bool = False
    persistent: bool = False

    def row(self, *buttons: Button) -> "Keyboard":
        if not buttons:
            raise ValueError("keyboard rows cannot be empty")
        self.rows.append(list(buttons))
        return self

    def add(self, *buttons: Button, width: int = 1) -> "Keyboard":
        if width < 1:
            raise ValueError("width must be positive")
        for index in range(0, len(buttons), width):
            self.row(*buttons[index:index + width])
        return self

    def to_dict(self, *, include_style: bool = False) -> dict[str, Any]:
        key = "inline_keyboard" if self.inline else "keyboard"
        payload: dict[str, Any] = {key: [[b.to_dict(include_style=include_style) for b in row] for row in self.rows]}
        if not self.inline:
            for name in ("resize_keyboard", "one_time_keyboard", "selective", "persistent"):
                payload[name] = getattr(self, name)
        return payload


def button(text: str, *, callback: str | None = None, url: str | None = None,
           style: ButtonStyle | str | None = None, **kwargs: Any) -> Button:
    """Convenience constructor using the shorter ``callback`` spelling."""
    return Button(text, callback_data=callback, url=url, style=style, **kwargs)


def inline(*rows: list[Button] | tuple[Button, ...]) -> Keyboard:
    return Keyboard(inline=True, rows=[list(row) for row in rows])


def reply(*rows: list[Button] | tuple[Button, ...], **options: Any) -> Keyboard:
    return Keyboard(inline=False, rows=[list(row) for row in rows], **options)
