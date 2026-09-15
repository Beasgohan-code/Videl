# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Group Administration & Moderation Plugin

import re
import asyncio
from datetime import datetime, timedelta
from pyrogram import enums, filters, types
from videl import app
from videl.helpers._admins import admin_check
from videl.helpers._utilities import extract_user
from videl.helpers.button_style import styled_button, ButtonStyle


def parse_time(time_str: str) -> int:
    unit = time_str[-1].lower()
    value = int(time_str[:-1])
    if unit == "m":
        return value * 60
    elif unit == "h":
        return value * 3600
    elif unit == "d":
        return value * 86400
    return value


@app.on_message(filters.command(["ban", "tban"]) & filters.group & ~app.bl_users)
@admin_check
async def ban_user(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("<b>Usage:</b> <code>/ban [reply / user_id / username] [optional: reason / time (e.g. 10m, 2h)]</code>")

    if user.id == app.id:
        return await message.reply_text("I cannot ban myself!")
    if user.id in app.sudoers:
        return await message.reply_text("Cannot ban a bot sudoer!")

    until_date = None
    reason = "No reason specified"
    if len(message.command) > 2:
        arg = message.command[-1]
        if re.match(r"^\d+[mhd]$", arg.lower()):
            seconds = parse_time(arg)
            until_date = datetime.utcnow() + timedelta(seconds=seconds)
            reason = " ".join(message.command[2:-1]) or "Temporary ban"
        else:
            reason = " ".join(message.command[2:])

    try:
        if until_date:
            await message.chat.ban_member(user.id, until_date=until_date)
            await message.reply_text(f"⏳ <b>Banned</b> {user.mention} temporarily until {until_date.strftime('%Y-%m-%d %H:%M:%S')} UTC.\n<b>Reason:</b> <code>{reason}</code>")
        else:
            await message.chat.ban_member(user.id)
            await message.reply_text(f"🚫 <b>Banned</b> {user.mention} from <b>{message.chat.title}</b>.\n<b>Reason:</b> <code>{reason}</code>")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Failed to ban:</b> <code>{ex}</code>")


@app.on_message(filters.command(["unban"]) & filters.group & ~app.bl_users)
@admin_check
async def unban_user(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("<b>Usage:</b> <code>/unban [reply / user_id / username]</code>")

    try:
        await message.chat.unban_member(user.id)
        await message.reply_text(f"✅ <b>Unbanned</b> {user.mention} in <b>{message.chat.title}</b>.")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Failed to unban:</b> <code>{ex}</code>")


@app.on_message(filters.command(["kick", "kickuser"]) & filters.group & ~app.bl_users)
@admin_check
async def kick_user(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("<b>Usage:</b> <code>/kick [reply / user_id / username]</code>")

    if user.id == app.id:
        return await message.reply_text("I cannot kick myself!")
    if user.id in app.sudoers:
        return await message.reply_text("Cannot kick a sudoer!")

    try:
        await message.chat.ban_member(user.id)
        await message.chat.unban_member(user.id)
        await message.reply_text(f"👢 <b>Kicked</b> {user.mention} from <b>{message.chat.title}</b>.")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Failed to kick:</b> <code>{ex}</code>")


@app.on_message(filters.command(["mute", "tmute"]) & filters.group & ~app.bl_users)
@admin_check
async def mute_user(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("<b>Usage:</b> <code>/mute [reply / user_id / username] [optional: time e.g. 10m, 1h]</code>")

    if user.id == app.id or user.id in app.sudoers:
        return await message.reply_text("Cannot mute this user!")

    until_date = None
    if len(message.command) > 2:
        arg = message.command[-1]
        if re.match(r"^\d+[mhd]$", arg.lower()):
            seconds = parse_time(arg)
            until_date = datetime.utcnow() + timedelta(seconds=seconds)

    try:
        permissions = types.ChatPermissions(can_send_messages=False)
        if until_date:
            await message.chat.restrict_member(user.id, permissions=permissions, until_date=until_date)
            await message.reply_text(f"🔇 <b>Muted</b> {user.mention} temporarily until {until_date.strftime('%Y-%m-%d %H:%M:%S')} UTC.")
        else:
            await message.chat.restrict_member(user.id, permissions=permissions)
            await message.reply_text(f"🔇 <b>Muted</b> {user.mention} indefinitely.")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Failed to mute:</b> <code>{ex}</code>")


@app.on_message(filters.command(["unmute"]) & filters.group & ~app.bl_users)
@admin_check
async def unmute_user(_, message: types.Message):
    user = await extract_user(message)
    if not user:
        return await message.reply_text("<b>Usage:</b> <code>/unmute [reply / user_id / username]</code>")

    try:
        permissions = types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        await message.chat.restrict_member(user.id, permissions=permissions)
        await message.reply_text(f"🔊 <b>Unmuted</b> {user.mention} successfully.")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Failed to unmute:</b> <code>{ex}</code>")


@app.on_message(filters.command(["pin", "unpin", "unpinall"]) & filters.group & ~app.bl_users)
@admin_check
async def pin_message(_, message: types.Message):
    cmd = message.command[0].lower()
    if cmd == "unpinall":
        try:
            await message.chat.unpin_all_messages()
            return await message.reply_text("📌 <b>Unpinned all messages in this group.</b>")
        except Exception as ex:
            return await message.reply_text(f"❌ <code>{ex}</code>")

    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin or unpin it.")

    try:
        if cmd == "pin":
            await message.reply_to_message.pin(disable_notification=False)
            await message.reply_text("📌 <b>Pinned message successfully!</b>")
        else:
            await message.reply_to_message.unpin()
            await message.reply_text("📌 <b>Unpinned message successfully!</b>")
    except Exception as ex:
        await message.reply_text(f"❌ <code>{ex}</code>")


@app.on_message(filters.command(["purge", "del"]) & filters.group & ~app.bl_users)
@admin_check
async def purge_messages(_, message: types.Message):
    if message.command[0].lower() == "del":
        if not message.reply_to_message:
            return await message.reply_text("Reply to a message to delete it.")
        try:
            await message.reply_to_message.delete()
            await message.delete()
        except Exception:
            pass
        return

    if not message.reply_to_message:
        return await message.reply_text("Reply to a starting message to purge up to this command.")

    start_id = message.reply_to_message.id
    end_id = message.id
    message_ids = list(range(start_id, end_id + 1))

    deleted = 0
    # Delete in batches of 100
    for i in range(0, len(message_ids), 100):
        batch = message_ids[i : i + 100]
        try:
            await app.delete_messages(chat_id=message.chat.id, message_ids=batch, revoke=True)
            deleted += len(batch)
        except Exception:
            pass

    status = await message.reply_text(f"🗑 <b>Purged {deleted} messages successfully!</b>")
    await asyncio.sleep(4)
    try:
        await status.delete()
    except Exception:
        pass


@app.on_message(filters.command(["staff", "adminlist", "admins"]) & filters.group & ~app.bl_users)
async def staff_list(_, message: types.Message):
    sent = await message.reply_text("👥 <i>Fetching group administrators...</i>")
    text = f"👑 <b><u>Staff in {message.chat.title}</u></b>\n\n<blockquote expandable>"
    creator = ""
    admins = []
    bots = []

    async for member in message.chat.get_members(filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if member.status == enums.ChatMemberStatus.OWNER:
            creator = f"<b>Owner:</b> {member.user.mention} (<code>{member.user.id}</code>)\n"
        elif member.user.is_bot:
            bots.append(f"🤖 {member.user.mention}")
        else:
            admins.append(f"👮‍♂️ {member.user.mention} (<code>{member.user.id}</code>)")

    text += creator
    if admins:
        text += "\n<b>Admins:</b>\n" + "\n".join(admins) + "\n"
    if bots:
        text += "\n<b>Bots:</b>\n" + "\n".join(bots) + "\n"
    text += "</blockquote>"

    await sent.edit_text(text)


@app.on_message(filters.command(["id", "info"]) & ~app.bl_users)
async def get_info(_, message: types.Message):
    user = await extract_user(message) or message.from_user
    chat = message.chat

    info_card = (
        f"👤 <b><u>User Information</u></b>\n\n"
        f"• <b>Name:</b> {user.first_name if user else 'N/A'}\n"
        f"• <b>Username:</b> @{user.username if user and user.username else 'None'}\n"
        f"• <b>User ID:</b> <code>{user.id if user else 0}</code>\n"
        f"• <b>Mention:</b> {user.mention if user else 'None'}\n\n"
        f"💬 <b><u>Chat Information</u></b>\n\n"
        f"• <b>Title:</b> {chat.title if chat.title else 'Private Chat'}\n"
        f"• <b>Chat ID:</b> <code>{chat.id}</code>\n"
        f"• <b>Type:</b> <code>{chat.type.name}</code>"
    )

    keyboard = types.InlineKeyboardMarkup([
        [
            styled_button(text="❐ Copy User ID", copy_text=str(user.id if user else 0), style=ButtonStyle.PRIMARY),
            styled_button(text="❐ Copy Chat ID", copy_text=str(chat.id), style=ButtonStyle.DEFAULT),
        ]
    ])
    await message.reply_text(info_card, reply_markup=keyboard, quote=True)
