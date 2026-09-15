# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Assistant Clean & Leave All Inactive Chats

import asyncio
from pyrogram import enums, filters, types
from videl import app, db, userbot


@app.on_message(filters.command(["leaveall", "assleaveall"]) & app.sudoers)
async def leave_all_chats(_, message: types.Message):
    sent = await message.reply_text("🧹 <i>Instructing assistants to leave non-active chats...</i>")
    total_left = 0

    for idx, ub in enumerate(userbot.clients, 1):
        left_count = 0
        try:
            async for dialog in ub.get_dialogs():
                if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
                    chat_id = dialog.chat.id
                    if chat_id in (app.logger_id, message.chat.id) or chat_id in db.active_calls:
                        continue
                    try:
                        await ub.leave_chat(chat_id)
                        left_count += 1
                        total_left += 1
                        await asyncio.sleep(1)
                    except Exception:
                        pass
        except Exception:
            pass

    await sent.edit_text(f"✅ <b>Assistants left {total_left} inactive chats successfully!</b>")
