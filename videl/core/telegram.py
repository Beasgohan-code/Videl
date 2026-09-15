# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Telegram Media Downloader

import asyncio
import os
import time
from pyrogram import types
from videl import config, logger
from videl.helpers._dataclass import Media
from videl.helpers._utilities import format_eta, format_size


class Telegram:
    def __init__(self):
        self.active_tasks = {}
        self.events = {}
        self.last_edit = {}
        self.sleep_interval = 5

    def get_media(self, msg: types.Message) -> bool:
        return bool(msg and (msg.video or msg.audio or msg.document or msg.voice))

    async def cancel(self, query: types.CallbackQuery):
        msg_id = query.message.id
        event = self.events.get(msg_id)
        task = self.active_tasks.pop(msg_id, None)
        if event:
            event.set()
        if task and not task.done():
            task.cancel()
        if event or task:
            await query.edit_message_text(
                query.lang["dl_cancel"].format(query.from_user.mention)
            )
        else:
            await query.answer(query.lang["dl_not_found"], show_alert=True)

    async def download(self, msg: types.Message, sent: types.Message) -> Media | None:
        from videl.helpers._inline import buttons
        msg_id = sent.id
        event = asyncio.Event()
        self.events[msg_id] = event
        self.last_edit[msg_id] = 0
        start_time = time.time()

        media_obj = msg.audio or msg.voice or msg.video or msg.document
        file_name = getattr(media_obj, "file_name", "Telegram_Audio.mp3") or "Telegram_Audio.mp3"
        file_size = getattr(media_obj, "file_size", 0)
        duration = getattr(media_obj, "duration", 0)
        video = bool(getattr(media_obj, "mime_type", "").startswith("video/"))
        title = getattr(media_obj, "title", file_name) or file_name

        if duration > config.DURATION_LIMIT:
            await sent.edit_text(sent.lang["play_duration_limit"].format(config.DURATION_LIMIT // 60))
            return None

        if file_size > 200 * 1024 * 1024:
            await sent.edit_text(sent.lang["dl_limit"])
            return None

        file_path = f"downloads/{sent.id}_{file_name}"

        async def progress(current, total):
            if event.is_set():
                raise asyncio.CancelledError()
            now = time.time()
            if (now - self.last_edit.get(msg_id, 0)) > self.sleep_interval:
                self.last_edit[msg_id] = now
                elapsed = now - start_time
                if elapsed <= 0:
                    return
                speed = current / elapsed
                percentage = (current / total) * 100
                eta = (total - current) / speed if speed > 0 else 0
                try:
                    await sent.edit_text(
                        text=sent.lang["dl_progress"].format(
                            format_size(current),
                            format_size(total),
                            percentage,
                            format_size(int(speed)),
                            format_eta(int(eta)),
                        ),
                        reply_markup=buttons.cancel_dl(sent.lang["cancel"]),
                    )
                except Exception:
                    pass

        try:
            task = asyncio.create_task(
                msg.download(file_name=file_path, progress=progress)
            )
            self.active_tasks[msg_id] = task
            await task
            self.active_tasks.pop(msg_id, None)
            self.events.pop(msg_id, None)

            return Media(
                id=str(sent.id),
                duration=time.strftime("%M:%S", time.gmtime(duration)) if duration else "00:00",
                duration_sec=duration,
                file_path=file_path,
                message_id=sent.id,
                title=title[:40],
                url="https://t.me",
                video=video,
            )
        except asyncio.CancelledError:
            if os.path.exists(file_path):
                os.remove(file_path)
            return None
        except Exception as ex:
            logger.error(f"Error downloading Telegram file: {ex}")
            if os.path.exists(file_path):
                os.remove(file_path)
            return None

    async def process_m3u8(self, url: str, message_id: int, video: bool = False) -> Media:
        return Media(
            id=str(message_id),
            duration="Live Stream",
            duration_sec=0,
            file_path=url,
            message_id=message_id,
            title="Live Stream",
            url=url,
            video=video,
        )
