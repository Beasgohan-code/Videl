# Videl

Videl is a lightweight, typed Telegram Bot API toolkit. The repository was empty at the start, so this first slice establishes a clean foundation instead of copying AviaxMusic's music-bot implementation.

## What's included

- `ButtonStyle`: semantic `PRIMARY`, `SECONDARY`, `SUCCESS`, `DANGER`, and `LINK` styles.
- `Button` and `Keyboard`: inline and reply keyboards with callback, URL, web app, login URL, and inline-query actions.
- `RichMessage`: fluent message composition with HTML/Markdown parse mode, keyboards, reply/thread options, and safe extra Bot API fields.
- `Bot`: small async client with injectable transport, so handlers are easy to test without Telegram or a live token.
- Validation for empty labels, mutually exclusive actions, and Telegram's 64-byte callback-data limit.

> Note: Telegram clients do not consistently support visual button colours. Videl preserves `ButtonStyle` for adapters, but omits `style` from normal Bot API payloads. Use `include_style=True` in a custom renderer when your target API supports it.

## Quick example

```python
from videl import Bot, ButtonStyle, RichMessage, button, inline

controls = inline(
    [button("▶ Play", callback="play", style=ButtonStyle.PRIMARY),
     button("⏭ Skip", callback="skip")],
    [button("Open channel", url="https://t.me/example")],
)
message = RichMessage("<b>Now playing</b>\nArtist — Track").buttons(controls)
bot = Bot("TOKEN")
await bot.send_message(chat_id, message)
```

Install locally with `pip install -e .`; run tests with `pip install -e '.[test]' && pytest`.

## Suggested next milestones

1. Add update routing and callback-query helpers.
2. Add media messages and a pluggable music provider (keeping provider/API keys out of the core).
3. Add rate limiting, retries, structured errors, and webhook/polling runners.
4. Add an optional adapter for Pyrogram/aiogram if Videl should power a full music bot like AviaxMusic.

AviaxMusic was reviewed as inspiration for the keyboard-driven music UX; its code is not copied into Videl.
