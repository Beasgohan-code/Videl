# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Global Broadcast Plugin

import os
import asyncio
from pyrogram import errors, filters, types
from videl import app, db, lang

broadcasting = False


@app.on_message(filters.command(["broadcast", "gcast"]) & app.sudoers)
@lang.language()
async def _broadcast(_, message: types.Message):
    global broadcasting
    if not message.reply_to_message:
        return await message.reply_text(message.lang["gcast_usage"])

    if broadcasting:
        return await message.reply_text(message.lang["gcast_active"])

    msg = message.reply_to_message
    count, ucount = 0, 0
    groups, users = [], []
    sent = await message.reply_text(message.lang["gcast_start"])

    if "-nochat" not in message.command:
        groups.extend(await db.get_chats())
    if "-user" in message.command:
        users.extend(await db.get_users())

    chats = list(set(groups + users))
    broadcasting = True

    try:
        await msg.forward(app.logger_id)
        log_msg = await app.send_message(
            chat_id=app.logger_id,
            text=message.lang["gcast_log"].format(
                message.from_user.id,
                message.from_user.mention,
                message.text,
            ),
        )
        await log_msg.pin(disable_notification=False)
    except Exception:
        pass

    await asyncio.sleep(2)
    failed = ""

    for chat in chats:
        if not broadcasting:
            await sent.edit_text(message.lang["gcast_stopped"].format(count, ucount))
            break

        try:
            if "-copy" in message.text:
                await msg.copy(chat, reply_markup=msg.reply_markup)
            else:
                await msg.forward(chat)

            if chat in groups:
                count += 1
            else:
                ucount += 1
            await asyncio.sleep(0.08)
        except errors.FloodWait as fw:
            await asyncio.sleep(fw.value + 15)
        except Exception as ex:
            failed += f"{chat} - {ex}\n"
            continue

    text = message.lang["gcast_end"].format(count, ucount)
    if failed:
        with open("broadcast_errors.txt", "w", encoding="utf-8") as f:
            f.write(failed)
        try:
            await message.reply_document(
                document="broadcast_errors.txt",
                caption=text,
            )
        except Exception:
            pass
        if os.path.exists("broadcast_errors.txt"):
            os.remove("broadcast_errors.txt")
    broadcasting = False
    await sent.edit_text(text)


@app.on_message(filters.command(["stop_gcast", "stop_broadcast"]) & app.sudoers)
@lang.language()
async def _stop_gcast(_, message: types.Message):
    global broadcasting
    if not broadcasting:
        return await message.reply_text(message.lang["gcast_inactive"])

    broadcasting = False
    try:
        log_msg = await app.send_message(
            chat_id=app.logger_id,
            text=message.lang["gcast_stop_log"].format(
                message.from_user.id,
                message.from_user.mention,
            ),
        )
        await log_msg.pin(disable_notification=False)
    except Exception:
        pass
    await message.reply_text(message.lang["gcast_stop"])
