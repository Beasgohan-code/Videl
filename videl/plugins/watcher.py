# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Group Voice Chat Event Watcher Plugin

from pyrogram import filters, types
from videl import anon, app, db, queue, userbot


@app.on_message(filters.video_chat_started)
async def vc_started_watcher(_, message: types.Message):
    try:
        if await db.is_clean_service(message.chat.id):
            await message.delete()
    except Exception:
        pass


@app.on_message(filters.video_chat_ended)
async def vc_ended_watcher(_, message: types.Message):
    try:
        await anon.stop(message.chat.id)
        if await db.is_clean_service(message.chat.id):
            await message.delete()
    except Exception:
        pass


@app.on_message(filters.video_chat_members_invited)
async def vc_invited_watcher(_, message: types.Message):
    try:
        if await db.is_clean_service(message.chat.id):
            await message.delete()
    except Exception:
        pass


@app.on_message(filters.left_chat_member)
async def assistant_kicked_watcher(_, message: types.Message):
    try:
        left_user = message.left_chat_member
        if left_user:
            # Check if left user is one of our assistants or bot
            assistant_ids = [ub.me.id for ub in userbot.clients if hasattr(ub, "me") and ub.me]
            if left_user.id == app.id or left_user.id in assistant_ids:
                queue.clear(message.chat.id)
                await db.remove_call(message.chat.id)
    except Exception:
        pass
