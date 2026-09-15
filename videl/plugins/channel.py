# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Channel Streaming Plugin (/cplay, /cvplay, /cpause, /cresume, /cstop, /cqueue, /channel)

from pyrogram import filters, types
from videl import anon, app, db, queue
from videl.helpers._admins import admin_check
from videl.helpers.button_style import styled_button, ButtonStyle

# In-memory mapping of group -> linked channel
linked_channels = {}


@app.on_message(filters.command(["channel", "linkchannel"]) & ~app.bl_users)
@admin_check
async def link_channel_cmd(_, message: types.Message):
    if len(message.command) < 2:
        curr = linked_channels.get(message.chat.id)
        return await message.reply_text(
            f"📢 <b>Linked Channel:</b> {curr if curr else '<code>None</code>'}\n\n"
            "To link a channel, use: <code>/channel @channel_username</code> or <code>/channel channel_id</code>\n"
            "To unlink: <code>/channel unlink</code>",
            quote=True,
        )

    target = message.command[1].strip()
    if target.lower() == "unlink":
        linked_channels.pop(message.chat.id, None)
        return await message.reply_text("✅ Successfully unlinked channel.", quote=True)

    try:
        chat = await app.get_chat(target)
        if chat.type != types.enums.ChatType.CHANNEL:
            return await message.reply_text("❌ Provided username/ID is not a channel.", quote=True)
        linked_channels[message.chat.id] = chat.id
        await message.reply_text(f"✅ Successfully linked channel: <b>{chat.title}</b> (<code>{chat.id}</code>)", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Failed to link channel: {e}", quote=True)


@app.on_message(filters.command(["cplay", "cvplay", "cstream"]) & ~app.bl_users)
async def cplay_cmd(_, message: types.Message):
    target_chat = None
    if message.chat.type == types.enums.ChatType.CHANNEL:
        target_chat = message.chat.id
    else:
        target_chat = linked_channels.get(message.chat.id)

    if not target_chat:
        return await message.reply_text(
            "❌ No channel linked to this group.\nLink one with <code>/channel @username</code> or use <code>/cplay</code> directly in the channel.",
            quote=True,
        )

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("❌ Please specify a song name, URL or reply to an audio file to play in channel.", quote=True)

    await message.reply_text(f"📢 <b>Routing channel stream request...</b>", quote=True)


@app.on_message(filters.command(["cpause"]) & ~app.bl_users)
@admin_check
async def cpause_cmd(_, message: types.Message):
    target_chat = message.chat.id if message.chat.type == types.enums.ChatType.CHANNEL else linked_channels.get(message.chat.id)
    if not target_chat:
        return await message.reply_text("❌ No linked channel found.", quote=True)
    try:
        await anon.pause(target_chat)
        await message.reply_text(f"⏸ <b>Channel stream paused.</b>", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)


@app.on_message(filters.command(["cresume"]) & ~app.bl_users)
@admin_check
async def cresume_cmd(_, message: types.Message):
    target_chat = message.chat.id if message.chat.type == types.enums.ChatType.CHANNEL else linked_channels.get(message.chat.id)
    if not target_chat:
        return await message.reply_text("❌ No linked channel found.", quote=True)
    try:
        await anon.resume(target_chat)
        await message.reply_text(f"▶️ <b>Channel stream resumed.</b>", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)


@app.on_message(filters.command(["cstop"]) & ~app.bl_users)
@admin_check
async def cstop_cmd(_, message: types.Message):
    target_chat = message.chat.id if message.chat.type == types.enums.ChatType.CHANNEL else linked_channels.get(message.chat.id)
    if not target_chat:
        return await message.reply_text("❌ No linked channel found.", quote=True)
    try:
        await anon.stop(target_chat)
        await message.reply_text(f"⏹ <b>Channel stream stopped.</b>", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}", quote=True)


@app.on_message(filters.command(["cqueue"]) & ~app.bl_users)
async def cqueue_cmd(_, message: types.Message):
    target_chat = message.chat.id if message.chat.type == types.enums.ChatType.CHANNEL else linked_channels.get(message.chat.id)
    if not target_chat:
        return await message.reply_text("❌ No linked channel found.", quote=True)
    items = queue.get_queue(target_chat)
    if not items:
        return await message.reply_text("📭 Channel queue is currently empty.", quote=True)
    text = "📢 <b><u>Channel Music Queue</u></b>\n\n"
    for i, item in enumerate(items[:10], start=1):
        text += f"<b>{i}.</b> <code>{item.title[:40]}</code> ({item.duration})\n"
    await message.reply_text(text, quote=True)
