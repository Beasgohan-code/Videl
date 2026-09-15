# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Global Ban (GBan) System Plugin

import asyncio
from pyrogram import filters, types
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from videl import app, db
from videl.helpers._utilities import extract_user


@app.on_message(filters.command(["gban", "globalban"]) & app.sudoers)
async def gban_cmd(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("❌ Please reply to a user or provide a user ID/username to GBan.", quote=True)

    if user.id in app.sudoers:
        return await message.reply_text("❌ You cannot GBan a sudo user or bot owner.", quote=True)

    if await db.is_gbanned(user.id):
        return await message.reply_text(f"❌ <b>{user.mention}</b> is already globally banned.", quote=True)

    reason = "Global Ban by Sudo"
    if len(message.command) > 2:
        reason = message.text.split(None, 2)[2]

    await db.add_gban(user.id, reason)
    msg = await message.reply_text(f"⚡ <b>Initiating Global Ban for {user.mention}...</b>", quote=True)

    banned_chats = 0
    served_chats = await db.get_chats()

    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user.id)
            banned_chats += 1
            await asyncio.sleep(0.05)
        except (ChatAdminRequired, UserAdminInvalid):
            continue
        except Exception:
            continue

    await msg.edit_text(
        f"🚨 <b><u>Global Ban Executed!</u></b>\n\n"
        f"👤 <b>Target:</b> {user.mention} (<code>{user.id}</code>)\n"
        f"🛡 <b>Enforced By:</b> {message.from_user.mention}\n"
        f"📝 <b>Reason:</b> <code>{reason}</code>\n"
        f"🌐 <b>Banned from:</b> <code>{banned_chats}</code> chats"
    )


@app.on_message(filters.command(["ungban", "unglobalban"]) & app.sudoers)
async def ungban_cmd(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("❌ Please reply to a user or provide a user ID/username to un-GBan.", quote=True)

    if not await db.is_gbanned(user.id):
        return await message.reply_text(f"❌ <b>{user.mention}</b> is not globally banned.", quote=True)

    await db.del_gban(user.id)
    msg = await message.reply_text(f"⚡ <b>Removing Global Ban for {user.mention}...</b>", quote=True)

    unbanned_chats = 0
    served_chats = await db.get_chats()

    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user.id)
            unbanned_chats += 1
            await asyncio.sleep(0.05)
        except Exception:
            continue

    await msg.edit_text(
        f"✅ <b><u>Global Ban Removed!</u></b>\n\n"
        f"👤 <b>Target:</b> {user.mention} (<code>{user.id}</code>)\n"
        f"🛡 <b>Unbanned from:</b> <code>{unbanned_chats}</code> chats"
    )


@app.on_message(filters.command(["gbanlist", "gbans"]) & app.sudoers)
async def gban_list_cmd(_, message: types.Message):
    gbanned = await db.get_gbanned()
    if not gbanned:
        return await message.reply_text("✅ No users are currently globally banned.", quote=True)

    text = f"🚨 <b><u>Globally Banned Users ({len(gbanned)})</u></b>\n\n<blockquote expandable>"
    for uid, reason in list(gbanned.items())[:50]:
        text += f"• <code>{uid}</code>: <i>{reason[:30]}</i>\n"
    if len(gbanned) > 50:
        text += f"\n<i>...and {len(gbanned) - 50} more users</i>"
    text += "</blockquote>"

    await message.reply_text(text, quote=True)


# Auto-Ban GBanned users when they join or send messages in groups
@app.on_message(filters.group & ~app.sudoers, group=100)
async def gban_auto_enforce(_, message: types.Message):
    if not message.from_user:
        return
    if await db.is_gbanned(message.from_user.id):
        try:
            await app.ban_chat_member(message.chat.id, message.from_user.id)
            await message.delete()
        except Exception:
            pass
