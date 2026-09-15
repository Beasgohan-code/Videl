# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Utility Functions & Loggers

import re
import aiohttp
from typing import Optional
from pyrogram import enums, types


def format_eta(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}:{seconds % 60:02d} min"
    else:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}:{m:02d}:{s:02d} h"


def format_size(bytes_len: int) -> str:
    if bytes_len >= 1024**3:
        return f"{bytes_len / 1024 ** 3:.2f} GB"
    elif bytes_len >= 1024**2:
        return f"{bytes_len / 1024 ** 2:.2f} MB"
    else:
        return f"{bytes_len / 1024:.2f} KB"


def to_seconds(time_str: str) -> int:
    try:
        parts = [int(p) for p in time_str.strip().split(":")]
        return sum(value * 60**i for i, value in enumerate(reversed(parts)))
    except Exception:
        return 0


def get_url(message: types.Message) -> Optional[str]:
    link = None
    messages = [message]
    if message.reply_to_message:
        messages.append(message.reply_to_message)

    for msg in messages:
        entities = msg.entities or msg.caption_entities or []
        for entity in entities:
            if entity.type == enums.MessageEntityType.TEXT_LINK:
                link = entity.url
                break
            elif entity.type == enums.MessageEntityType.URL:
                text = msg.text or msg.caption or ""
                link = text[entity.offset: entity.offset + entity.length]
                break

    if link:
        return link.split("&si")[0].split("?si")[0]
    return None


async def extract_user(msg: types.Message) -> Optional[types.User]:
    from videl import app
    if msg.reply_to_message and msg.reply_to_message.from_user:
        return msg.reply_to_message.from_user

    if msg.entities:
        for e in msg.entities:
            if e.type == enums.MessageEntityType.TEXT_MENTION and e.user:
                return e.user

    if msg.text:
        try:
            if match := re.search(r"@(\w{5,32})", msg.text):
                return await app.get_users(match.group(0))
            if match := re.search(r"\b\d{6,15}\b", msg.text):
                return await app.get_users(int(match.group(0)))
        except Exception:
            pass

    return None


async def play_log(m: types.Message, link: str, title: str, duration: str) -> None:
    from videl import app
    if m.chat.id == app.logger_id:
        return
    text = m.lang["play_log"].format(
        app.name,
        m.chat.id,
        m.chat.title,
        m.from_user.id if m.from_user else 0,
        m.from_user.mention if m.from_user else "Anonymous",
        link,
        title,
        duration,
    )
    try:
        await app.send_message(chat_id=app.logger_id, text=text)
    except Exception:
        pass


async def send_log(m: types.Message, chat: bool = False) -> None:
    from videl import app
    if chat:
        user = m.from_user
        text = m.lang["log_chat"].format(
            m.chat.id,
            m.chat.title,
            user.id if user else 0,
            user.mention if user else "Anonymous",
        )
    else:
        text = m.lang["log_user"].format(
            m.from_user.id,
            f"@{m.from_user.username}" if m.from_user.username else "",
            m.from_user.mention,
        )
    try:
        await app.send_message(chat_id=app.logger_id, text=text)
    except Exception:
        pass


async def fetch_lyrics(title: str) -> Optional[str]:
    """Fetch lyrics for song query."""
    try:
        clean_title = re.sub(r"\(.*?\)|\[.*?\]", "", title).strip()
        url = f"https://lyrist.vercel.app/api/{clean_title}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("lyrics")
    except Exception:
        pass
    return None
