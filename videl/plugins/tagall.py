# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Tag All & Member Notifier Plugin

import asyncio
from pyrogram import enums, filters, types
from videl import app
from videl.helpers._admins import admin_check

tagging_chats = set()


@app.on_message(filters.command(["tagall", "mention", "all", "utag"]) & filters.group & ~app.bl_users)
@admin_check
async def tag_all_members(_, message: types.Message):
    chat_id = message.chat.id
    if chat_id in tagging_chats:
        return await message.reply_text("⚠️ Tagging is already ongoing in this group! Use <code>/cancel_tagall</code> to stop it.")

    text_prompt = message.text.split(None, 1)[1] if len(message.command) > 1 else "Attention everyone!"
    tagging_chats.add(chat_id)

    status_msg = await message.reply_text(f"📢 <i>Starting mention spree...</i>\n<b>Prompt:</b> <code>{text_prompt}</code>")
    members_batch = []
    total_tagged = 0

    try:
        async for member in message.chat.get_members():
            if chat_id not in tagging_chats:
                break
            if member.user.is_bot or member.user.is_deleted:
                continue

            members_batch.append(f"• {member.user.mention}")
            if len(members_batch) == 5:
                tag_text = f"✨ <b>{text_prompt}</b>\n\n" + "\n".join(members_batch)
                await app.send_message(chat_id, tag_text)
                total_tagged += len(members_batch)
                members_batch.clear()
                await asyncio.sleep(2)

        if members_batch and chat_id in tagging_chats:
            tag_text = f"✨ <b>{text_prompt}</b>\n\n" + "\n".join(members_batch)
            await app.send_message(chat_id, tag_text)
            total_tagged += len(members_batch)

        await message.reply_text(f"✅ <b>Mention spree finished!</b> Mentioned {total_tagged} members.")
    except Exception as ex:
        await message.reply_text(f"❌ <b>Error:</b> <code>{ex}</code>")
    finally:
        tagging_chats.discard(chat_id)


@app.on_message(filters.command(["cancel_tagall", "stoptag", "untag"]) & filters.group & ~app.bl_users)
@admin_check
async def cancel_tagall(_, message: types.Message):
    chat_id = message.chat.id
    if chat_id not in tagging_chats:
        return await message.reply_text("❌ No active tagging spree to cancel.")

    tagging_chats.discard(chat_id)
    await message.reply_text("🛑 <b>Mention spree stopped!</b>")
