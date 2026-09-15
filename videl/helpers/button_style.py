# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot API ButtonStyle System

from enum import Enum
from typing import Optional, Union, List, Dict, Any

try:
    from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
except ImportError:
    class InlineKeyboardButton:
        def __init__(self, text: str, **kwargs):
            self.text = text
            for k, v in kwargs.items():
                setattr(self, k, v)

    class InlineKeyboardMarkup:
        def __init__(self, inline_keyboard: List[List[Any]]):
            self.inline_keyboard = inline_keyboard

    class WebAppInfo:
        def __init__(self, url: str):
            self.url = url


class ButtonStyle(str, Enum):
    """
    Represents Telegram Bot API button styles (primary, danger, success, default).
    Supported in Telegram Bot API 8.0+ / 10.0+ / Kurigram.
    """
    PRIMARY = "primary"
    DANGER = "danger"
    SUCCESS = "success"
    DEFAULT = "default"


class StyledInlineKeyboardButton(InlineKeyboardButton):
    """
    Enhanced InlineKeyboardButton supporting:
    - style (primary, danger, success, default)
    - copy_text (1-tap clipboard copy)
    - icon_custom_emoji_id (Telegram Custom Emoji icon)
    - web_app (Telegram Mini App)
    - callback_data & url
    """
    def __init__(
        self,
        text: str,
        callback_data: Optional[Union[str, bytes]] = None,
        url: Optional[str] = None,
        copy_text: Optional[str] = None,
        web_app: Optional[WebAppInfo] = None,
        style: Optional[Union[ButtonStyle, str]] = None,
        icon_custom_emoji_id: Optional[str] = None,
        user_id: Optional[int] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        **kwargs,
    ):
        style_val = style.value if isinstance(style, ButtonStyle) else style
        
        super().__init__(
            text=text,
            callback_data=callback_data,
            url=url,
            web_app=web_app,
            user_id=user_id,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            **kwargs,
        )
        self.style = style_val
        self.copy_text = copy_text
        self.icon_custom_emoji_id = icon_custom_emoji_id

    def write(self) -> Dict[str, Any]:
        """Convert button to Telegram Bot API JSON payload dict."""
        data = {"text": self.text}
        if getattr(self, "callback_data", None) is not None:
            cb = self.callback_data
            data["callback_data"] = cb if isinstance(cb, str) else cb.decode()
        if getattr(self, "url", None) is not None:
            data["url"] = self.url
        if self.copy_text is not None:
            data["copy_text"] = {"text": self.copy_text} if isinstance(self.copy_text, str) else self.copy_text
        if getattr(self, "web_app", None) is not None:
            data["web_app"] = {"url": self.web_app.url} if hasattr(self.web_app, "url") else self.web_app
        if self.style is not None:
            data["style"] = self.style
        if self.icon_custom_emoji_id is not None:
            data["icon_custom_emoji_id"] = self.icon_custom_emoji_id
        if getattr(self, "user_id", None) is not None:
            data["user_id"] = self.user_id
        if getattr(self, "switch_inline_query", None) is not None:
            data["switch_inline_query"] = self.switch_inline_query
        if getattr(self, "switch_inline_query_current_chat", None) is not None:
            data["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        return data


def styled_button(
    text: str,
    callback_data: Optional[str] = None,
    url: Optional[str] = None,
    copy_text: Optional[str] = None,
    style: Optional[Union[ButtonStyle, str]] = None,
    web_app_url: Optional[str] = None,
    icon_emoji_id: Optional[str] = None,
) -> StyledInlineKeyboardButton:
    """Helper factory for creating styled inline buttons."""
    web_app = WebAppInfo(url=web_app_url) if web_app_url else None
    return StyledInlineKeyboardButton(
        text=text,
        callback_data=callback_data,
        url=url,
        copy_text=copy_text,
        web_app=web_app,
        style=style,
        icon_custom_emoji_id=icon_emoji_id,
    )


def styled_keyboard(rows: List[List[StyledInlineKeyboardButton]]) -> InlineKeyboardMarkup:
    """Helper factory for creating inline keyboard markup."""
    return InlineKeyboardMarkup(rows)
