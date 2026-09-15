"""Videl: a focused, typed Telegram Bot API toolkit."""
from .buttons import Button, ButtonStyle, Keyboard, button, inline, reply
from .client import Bot
from .rich_message import RichMessage

__all__ = ["Bot", "Button", "ButtonStyle", "Keyboard", "RichMessage", "button", "inline", "reply"]
__version__ = "0.1.0"
