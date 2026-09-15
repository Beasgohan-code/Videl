# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Welcome Manager & Clean Service Messages Plugin

from pyrogram import enums, filters, types
from videl import app, db
from videl.helpers._admins import admin_check
from videl.helpers.button_style import styled_button, ButtonStyle


@app.on_message(filters.command(["setwelcome"]) & filters.group & ~app.bl_users)
@admin_check
async def set_welcome_cmd(_, message: types.Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "<b>Usage:</b> <code>/setwelcome [welcome text]</code>\n\n"
            "<b>Supported Placeholders:</b>\n"
            "• <code>{name}</code> - User's first name\n"
            "• <code>{mention}</code> - User's clickable mention\n"
            "• <code>{chat}</code> - Chat title\n"
            "• <code>{id}</code> - User numeric ID",
            quote=True,
        )

    text = message.text.split(None, 1)[1] if len(message.command) > 1 else message.reply_to_message.text
    await db.set_welcome(message.chat.id, text)
    await message.reply_text("✅ <b>Custom welcome message saved successfully!</b>", quote=True)


@app.on_message(filters.command(["delwelcome", "resetwelcome"]) & filters.group & ~app.bl_users)
@admin_check
async def del_welcome_cmd(_, message: types.Message):
    await db.del_welcome(message.chat.id)
    await message.reply_text("🗑 <b>Welcome message deleted. Reset to default greeting.</b>", quote=True)


@app.on_message(filters.command(["cleanservice"]) & filters.group & ~app.bl_users)
@admin_check
async def clean_service_cmd(_, message: types.Message):
    if len(message.command) < 2 or message.command[1].lower() not in ("on", "off"):
        status = await db.get_clean_service(message.chat.id)
        return await message.reply_text(
            f"🧹 <b>Clean Service Messages:</b> <code>{'Enabled' if status else 'Disabled'}</code>\n\n"
            "Use <code>/cleanservice on</code> or <code>/cleanservice off</code> to toggle auto-deletion of join/leave/pinned service messages.",
            quote=True,
        )

    enable = message.command[1].lower() == "on"
    await db.set_clean_service(message.chat.id, enable)
    await message.reply_text(f"🧹 <b>Clean Service Messages:</b> <code>{'Enabled' if enable else 'Disabled'}</code>", quote=True)


@app.on_message(filters.new_chat_members, group=10)
async def welcome_watcher(_, message: types.Message):
    # If clean service enabled, remove service join message
    if await db.get_clean_service(message.chat.id):
        try:
            await message.delete()
        except Exception:
            pass

    welcome_text = await db.get_welcome(message.chat.id)
    if not welcome_text:
        return

    for member in message.new_chat_members:
        if member.id == app.id:
            continue

        formatted = (
            welcome_text.replace("{name}", member.first_name)
            .replace("{mention}", member.mention)
            .replace("{chat}", message.chat.title)
            .replace("{id}", str(member.id))
        )
        try:
            await message.reply_text(formatted)
        except Exception:
            pass


@app.on_message(filters.left_chat_member | filters.pinned_message, group=11)
async def service_cleaner(_, message: types.Message):
    if await db.get_clean_service(message.chat.id):
        try:
            await message.delete()
        except Exception:
            pass
