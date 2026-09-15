# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl PyTgCalls Voice & Video Stream Engine

import time
from typing import List, Optional, Union
from ntgcalls import (
    ConnectionNotFound,
    TelegramServerError,
    RTMPStreamingUnsupported,
    ConnectionError as NTgConnectionError,
)
import pyrogram.errors as py_err
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls import PyTgCalls, exceptions, types
from pytgcalls.pytgcalls_session import PyTgCallsSession

ChatSendMediaForbidden = getattr(py_err, "ChatSendMediaForbidden", Exception)
ChatSendPhotosForbidden = getattr(py_err, "ChatSendPhotosForbidden", ChatSendMediaForbidden)
MessageIdInvalid = getattr(py_err, "MessageIdInvalid", Exception)

from videl import (
    app,
    config,
    db,
    lang,
    logger,
    queue,
    thumb,
    userbot,
    yt,
)
from videl.helpers._dataclass import Media, Track


def format_player_caption(media: Union[Media, Track], played_sec: int = 1) -> str:
    total_sec = media.duration_sec or 0
    bar_len = 12
    if total_sec > 0:
        ratio = min(max(played_sec / total_sec, 0.0), 1.0)
        pos = min(int(ratio * bar_len), bar_len - 1)
        progress_bar = "─" * pos + "🔘" + "─" * (bar_len - pos - 1)
        played_str = time.strftime("%M:%S", time.gmtime(played_sec))
        total_str = media.duration or time.strftime("%M:%S", time.gmtime(total_sec))
    else:
        progress_bar = "🔘───────────"
        played_str = "0:01"
        total_str = "Live"

    m_type = "VIDEO" if media.video else "AUDIO"
    channel = getattr(media, "channel_name", "") or "Videl Stream"
    user_mention = media.user or "Anonymous"

    caption = (
        f"<b><a href='{media.url}'>{media.title}</a></b>\n"
        f"{channel}\n"
        f"<i>{m_type} • {media.duration or 'Live'}</i>\n"
        f"Requested by {user_mention} 🤍\n\n"
        f"<code>{played_str} {progress_bar} {total_str}</code>"
    )
    return caption


class TgCall(PyTgCalls):
    def __init__(self):
        self.clients: List[PyTgCalls] = []

    async def pause(self, chat_id: int) -> bool:
        client = await db.get_assistant(chat_id)
        await db.playing(chat_id, paused=True)
        return await client.pause(chat_id)

    async def resume(self, chat_id: int) -> bool:
        client = await db.get_assistant(chat_id)
        await db.playing(chat_id, paused=False)
        return await client.resume(chat_id)

    async def stop(self, chat_id: int) -> None:
        try:
            client = await db.get_assistant(chat_id)
            queue.clear(chat_id)
            await db.remove_call(chat_id)
            await db.set_loop(chat_id, 0)
            await client.leave_call(chat_id, close=False)
        except Exception:
            pass

    async def change_volume(self, chat_id: int, volume: int) -> bool:
        try:
            client = await db.get_assistant(chat_id)
            await db.set_volume(chat_id, volume)
            return await client.change_volume_call(chat_id, volume)
        except Exception:
            return False

    async def play_media(
        self,
        chat_id: int,
        message: Message,
        media: Union[Media, Track],
        seek_time: int = 0,
    ) -> None:
        from videl.helpers._inline import buttons

        client = await db.get_assistant(chat_id)
        _lang = await lang.get_lang(chat_id)
        _thumb = (
            await thumb.generate(media)
            if isinstance(media, Track)
            else config.DEFAULT_THUMB
        ) if config.THUMB_GEN else None

        if not media.file_path:
            await message.edit_text(_lang["error_no_file"].format(config.SUPPORT_CHAT))
            return await self.play_next(chat_id)

        stream = types.MediaStream(
            media_path=media.file_path,
            audio_parameters=types.AudioQuality.HIGH,
            video_parameters=types.VideoQuality.HD_720p,
            audio_flags=types.MediaStream.Flags.REQUIRED,
            video_flags=(
                types.MediaStream.Flags.AUTO_DETECT
                if media.video
                else types.MediaStream.Flags.IGNORE
            ),
            ffmpeg_parameters=f"-ss {seek_time}" if seek_time > 1 else None,
        )

        try:
            await client.play(
                chat_id=chat_id,
                stream=stream,
                config=types.GroupCallConfig(auto_start=False),
            )
            if not seek_time:
                media.time = 1
                await db.add_call(chat_id)
                text = format_player_caption(media, played_sec=1)
                q_len = max(0, len(queue.get_queue(chat_id)) - 1)
                keyboard = buttons.controls(
                    chat_id,
                    queue_count=q_len,
                    song_url=media.url,
                    is_playing=True,
                )
                try:
                    if _thumb:
                        await message.edit_media(
                            media=InputMediaPhoto(media=_thumb, caption=text),
                            reply_markup=keyboard,
                        )
                    else:
                        await message.edit_text(text, reply_markup=keyboard)
                except (ChatSendMediaForbidden, ChatSendPhotosForbidden, MessageIdInvalid):
                    if _thumb:
                        sent = await app.send_photo(
                            chat_id=chat_id,
                            photo=_thumb,
                            caption=text,
                            reply_markup=keyboard,
                        )
                    else:
                        sent = await app.send_message(
                            chat_id=chat_id,
                            text=text,
                            reply_markup=keyboard,
                        )
                    media.message_id = sent.id
        except FileNotFoundError:
            await message.edit_text(_lang["error_no_file"].format(config.SUPPORT_CHAT))
            await self.play_next(chat_id)
        except exceptions.NoActiveGroupCall:
            await self.stop(chat_id)
            await message.edit_text(_lang["error_no_call"])
        except exceptions.NoAudioSourceFound:
            await message.edit_text(_lang["error_no_audio"])
            await self.play_next(chat_id)
        except (NTgConnectionError, ConnectionNotFound, TelegramServerError):
            await self.stop(chat_id)
            await message.edit_text(_lang["error_tg_server"])
        except RTMPStreamingUnsupported:
            await self.stop(chat_id)
            await message.edit_text(_lang["error_rtmp"])

    async def replay(self, chat_id: int) -> None:
        if not await db.get_call(chat_id):
            return

        media = queue.get_current(chat_id)
        if not media:
            return
        _lang = await lang.get_lang(chat_id)
        msg = await app.send_message(chat_id=chat_id, text=_lang["play_again"])
        media.message_id = msg.id
        await self.play_media(chat_id, msg, media)

    async def play_next(self, chat_id: int) -> None:
        if loop := await db.get_loop(chat_id):
            await db.set_loop(chat_id, loop - 1)
            return await self.replay(chat_id)

        media = queue.get_next(chat_id)
        try:
            if media and media.message_id:
                await app.delete_messages(
                    chat_id=chat_id,
                    message_ids=media.message_id,
                    revoke=True,
                )
                media.message_id = 0
        except Exception:
            pass

        if not media:
            return await self.stop(chat_id)

        _lang = await lang.get_lang(chat_id)
        msg = await app.send_message(chat_id=chat_id, text=_lang["play_next"])
        if not media.file_path:
            media.file_path = await yt.download(media.id, video=media.video)
            if not media.file_path:
                await self.play_next(chat_id)
                return await msg.edit_text(
                    _lang["error_no_file"].format(config.SUPPORT_CHAT)
                )

        media.message_id = msg.id
        await self.play_media(chat_id, msg, media)

    async def ping(self) -> float:
        if not self.clients:
            return 0.0
        pings = [client.ping for client in self.clients]
        return round(sum(pings) / len(pings), 2)

    async def decorators(self, client: PyTgCalls) -> None:
        @client.on_update()
        async def update_handler(_, update: types.Update) -> None:
            if isinstance(update, types.StreamEnded):
                if update.stream_type == types.StreamEnded.Type.AUDIO:
                    await self.play_next(update.chat_id)
            elif isinstance(update, types.ChatUpdate):
                if update.status in [
                    types.ChatUpdate.Status.KICKED,
                    types.ChatUpdate.Status.LEFT_GROUP,
                    types.ChatUpdate.Status.CLOSED_VOICE_CHAT,
                ]:
                    await self.stop(update.chat_id)

    async def boot(self) -> None:
        PyTgCallsSession.notice_displayed = True
        for ub in userbot.clients:
            client = PyTgCalls(ub, cache_duration=100)
            await client.start()
            self.clients.append(client)
            await self.decorators(client)
        logger.info(f"PyTgCalls initialized with {len(self.clients)} client(s).")
