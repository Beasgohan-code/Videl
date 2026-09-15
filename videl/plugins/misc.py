# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Background Watchers & Timers

import asyncio
import time
from pyrogram import enums, errors, filters, types
from videl import (
    anon,
    app,
    config,
    db,
    lang,
    queue,
    tasks,
    userbot,
    yt,
)
from videl.helpers._inline import buttons


@app.on_message(filters.video_chat_started, group=19)
@app.on_message(filters.video_chat_ended, group=20)
async def _watcher_vc(_, m: types.Message):
    await anon.stop(m.chat.id)


async def auto_leave():
    while True:
        await asyncio.sleep(3600)
        for ub in userbot.clients:
            try:
                chats = [
                    dialog.chat.id
                    async for dialog in ub.get_dialogs()
                    if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP)
                ][-20:]
                for chat in chats:
                    if chat in [app.logger_id, -1001686672798, -1001549206010]:
                        continue
                    if chat in db.active_calls:
                        continue
                    await ub.leave_chat(chat)
                    await asyncio.sleep(5)
            except asyncio.CancelledError:
                raise
            except Exception:
                continue


async def track_time():
    while True:
        await asyncio.sleep(1)
        for chat_id in list(db.active_calls):
            if not await db.playing(chat_id):
                continue
            media = queue.get_current(chat_id)
            if not media:
                continue
            media.time += 1


async def update_timer(length=12):
    while True:
        await asyncio.sleep(7)
        for chat_id in list(db.active_calls):
            if not await db.playing(chat_id):
                continue
            try:
                media = queue.get_current(chat_id)
                if not media:
                    continue
                duration, message_id = media.duration_sec, media.message_id
                if not duration or not message_id or not media.time:
                    continue

                played = media.time
                remaining = max(0, duration - played)
                pos = min(int((played / duration) * length), length - 1)
                bar = "═" * pos + "🔘" + "═" * (length - pos - 1)

                if remaining <= 30:
                    nxt = queue.get_next(chat_id, check=True)
                    if nxt and not nxt.file_path:
                        nxt.file_path = await yt.download(nxt.id, video=nxt.video)

                if remaining < 10:
                    remove = True
                    timer_str = None
                else:
                    if config.THUMB_GEN:
                        timer_str = f"{time.strftime('%M:%S', time.gmtime(played))} ┃ {bar} ┃ -{time.strftime('%M:%S', time.gmtime(remaining))}"
                    else:
                        timer_str = None
                    remove = False

                if not timer_str and not remove:
                    continue

                is_p = await db.playing(chat_id)
                await app.edit_message_reply_markup(
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=buttons.controls(
                        chat_id=chat_id, timer=timer_str, remove=remove, is_playing=is_p
                    ),
                )
            except asyncio.CancelledError:
                raise
            except Exception:
                pass


async def vc_watcher(sleep=15):
    while True:
        await asyncio.sleep(sleep)
        for chat_id in list(db.active_calls):
            try:
                client = await db.get_assistant(chat_id)
                media = queue.get_current(chat_id)
                if not media:
                    continue
                participants = await client.get_participants(chat_id)
                if len(participants) < 2 and media.time > 30:
                    _lang = await lang.get_lang(chat_id)
                    try:
                        sent = await app.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=media.message_id,
                            reply_markup=buttons.controls(
                                chat_id=chat_id, status=_lang["stopped"], remove=True
                            ),
                        )
                        await anon.stop(chat_id)
                        await sent.reply_text(_lang["auto_left"])
                    except errors.MessageIdInvalid:
                        pass
            except asyncio.CancelledError:
                raise
            except Exception:
                pass


def init_tasks():
    """Start background scheduler tasks if not already running."""
    try:
        loop = asyncio.get_running_loop()
        if config.AUTO_END:
            tasks.append(loop.create_task(vc_watcher()))
        if config.AUTO_LEAVE:
            tasks.append(loop.create_task(auto_leave()))
        tasks.append(loop.create_task(track_time()))
        tasks.append(loop.create_task(update_timer()))
    except RuntimeError:
        pass


init_tasks()
