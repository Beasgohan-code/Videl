# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Group Filters & Notes Manager Plugin

import re
from pyrogram import filters, types
from videl import app, db
from videl.helpers._admins import admin_check


@app.on_message(filters.command(["filter"]) & filters.group & ~app.bl_users)
@admin_check
async def add_filter(_, message: types.Message):
    if len(message.command) < 3 and not (len(message.command) == 2 and message.reply_to_message):
        return await message.reply_text("<b>Usage:</b> <code>/filter [keyword] [reply text]</code> or reply to a message with <code>/filter [keyword]</code>", quote=True)

    keyword = message.command[1].lower()
    reply_text = message.text.split(None, 2)[2] if len(message.command) > 2 else message.reply_to_message.text

    await db.set_filter(message.chat.id, keyword, reply_text)
    await message.reply_text(f"✅ <b>Filter saved for:</b> <code>{keyword}</code>", quote=True)


@app.on_message(filters.command(["stopfilter", "stop"]) & filters.group & ~app.bl_users)
@admin_check
async def remove_filter(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/stopfilter [keyword]</code>", quote=True)

    keyword = message.command[1].lower()
    removed = await db.del_filter(message.chat.id, keyword)
    if removed:
        await message.reply_text(f"🗑 <b>Filter removed for:</b> <code>{keyword}</code>", quote=True)
    else:
        await message.reply_text("❌ No such filter exists in this group.", quote=True)


@app.on_message(filters.command(["filters"]) & filters.group & ~app.bl_users)
async def list_filters(_, message: types.Message):
    all_filters = await db.get_filters(message.chat.id)
    if not all_filters:
        return await message.reply_text("❌ No active keyword filters in this chat.", quote=True)

    text = f"✨ <b><u>Active Filters in {message.chat.title}</u></b>\n\n<blockquote expandable>"
    for kw in sorted(all_filters.keys()):
        text += f"• <code>{kw}</code>\n"
    text += "</blockquote>"
    await message.reply_text(text, quote=True)


@app.on_message(filters.command(["save", "note"]) & filters.group & ~app.bl_users)
@admin_check
async def save_note(_, message: types.Message):
    if len(message.command) < 3 and not (len(message.command) == 2 and message.reply_to_message):
        return await message.reply_text("<b>Usage:</b> <code>/save [note_name] [content]</code> or reply to a message with <code>/save [note_name]</code>", quote=True)

    name = message.command[1].lower()
    content = message.text.split(None, 2)[2] if len(message.command) > 2 else message.reply_to_message.text

    await db.set_note(message.chat.id, name, content)
    await message.reply_text(f"📌 <b>Note saved:</b> <code>{name}</code>\nGet it with <code>/get {name}</code> or <code>#{name}</code>", quote=True)


@app.on_message(filters.command(["get"]) & filters.group & ~app.bl_users)
async def get_note_cmd(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/get [note_name]</code>", quote=True)

    name = message.command[1].lower()
    all_notes = await db.get_notes(message.chat.id)
    content = all_notes.get(name)
    if content:
        await message.reply_text(content, quote=True)
    else:
        await message.reply_text("❌ Note not found.", quote=True)


@app.on_message(filters.command(["clear", "delnote"]) & filters.group & ~app.bl_users)
@admin_check
async def clear_note(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/clear [note_name]</code>", quote=True)

    name = message.command[1].lower()
    removed = await db.del_note(message.chat.id, name)
    if removed:
        await message.reply_text(f"🗑 <b>Note deleted:</b> <code>{name}</code>", quote=True)
    else:
        await message.reply_text("❌ Note not found.", quote=True)


@app.on_message(filters.command(["notes"]) & filters.group & ~app.bl_users)
async def list_notes(_, message: types.Message):
    all_notes = await db.get_notes(message.chat.id)
    if not all_notes:
        return await message.reply_text("❌ No saved notes in this chat.", quote=True)

    text = f"📝 <b><u>Saved Notes in {message.chat.title}</u></b>\n\n<blockquote expandable>"
    for name in sorted(all_notes.keys()):
        text += f"• <code>#{name}</code>\n"
    text += "</blockquote>"
    await message.reply_text(text, quote=True)


@app.on_message(filters.group & ~filters.me, group=14)
async def filter_responder(_, message: types.Message):
    if not message.text:
        return

    # Check hashtag notes
    if message.text.startswith("#") and len(message.text) > 1:
        tag = message.text[1:].split()[0].lower()
        notes = await db.get_notes(message.chat.id)
        if tag in notes:
            return await message.reply_text(notes[tag], quote=True)

    # Check keyword filters
    chat_filters = await db.get_filters(message.chat.id)
    if not chat_filters:
        return

    words = message.text.lower().split()
    for kw, reply in chat_filters.items():
        if kw in words or kw == message.text.lower():
            try:
                await message.reply_text(reply, quote=True)
            except Exception:
                pass
            break
