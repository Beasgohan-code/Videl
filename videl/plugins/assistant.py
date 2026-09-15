# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Assistant Profile & Session Manager Plugin

import os
from pyrogram import filters, types
from videl import app, config, userbot


@app.on_message(filters.command(["setpfp", "asspfp"]) & app.sudoers)
async def set_pfp_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("❌ Please reply to a photo to update the assistant profile picture.", quote=True)

    msg = await message.reply_text("⚡ Updating assistant profile picture...", quote=True)
    photo_path = await message.reply_to_message.download()

    success_count = 0
    for ub in userbot.clients:
        try:
            await ub.set_profile_photo(photo=photo_path)
            success_count += 1
        except Exception:
            pass

    if os.path.exists(photo_path):
        os.remove(photo_path)

    await msg.edit_text(f"✅ Successfully updated profile picture for <b>{success_count}</b> assistant(s)!")


@app.on_message(filters.command(["delpfp", "delasspfp"]) & app.sudoers)
async def del_pfp_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    msg = await message.reply_text("⚡ Deleting assistant profile picture...", quote=True)
    deleted_count = 0
    for ub in userbot.clients:
        try:
            photos = [p async for p in ub.get_chat_photos("me")]
            if photos:
                await ub.delete_profile_photos(photos[0].file_id)
                deleted_count += 1
        except Exception:
            pass

    await msg.edit_text(f"✅ Deleted profile picture for <b>{deleted_count}</b> assistant(s)!")


@app.on_message(filters.command(["setname", "assname"]) & app.sudoers)
async def set_name_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: <code>/setname [New First Name] [Optional Last Name]</code>", quote=True)

    names = message.text.split(None, 2)[1:]
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ""

    msg = await message.reply_text("⚡ Updating assistant display name...", quote=True)
    updated = 0
    for ub in userbot.clients:
        try:
            await ub.update_profile(first_name=first_name, last_name=last_name)
            updated += 1
        except Exception:
            pass

    await msg.edit_text(f"✅ Successfully updated display name for <b>{updated}</b> assistant(s) to <b>{first_name} {last_name}</b>!")


@app.on_message(filters.command(["setbio", "assbio"]) & app.sudoers)
async def set_bio_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: <code>/setbio [Bio Text]</code>", quote=True)

    bio = message.text.split(None, 1)[1]
    msg = await message.reply_text("⚡ Updating assistant profile bio...", quote=True)
    updated = 0
    for ub in userbot.clients:
        try:
            await ub.update_profile(bio=bio[:70])
            updated += 1
        except Exception:
            pass

    await msg.edit_text(f"✅ Successfully updated bio for <b>{updated}</b> assistant(s)!")


@app.on_message(filters.command(["userbotjoin", "assjoin"]) & app.sudoers)
async def userbot_join_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = message.command[1]

    msg = await message.reply_text(f"⚡ Joining target chat with assistant...", quote=True)
    client = userbot.clients[0]
    try:
        await client.join_chat(chat_id)
        await msg.edit_text(f"✅ Assistant successfully joined <code>{chat_id}</code>!")
    except Exception as e:
        await msg.edit_text(f"❌ Failed to join chat: {e}")


@app.on_message(filters.command(["userbotleave", "assleave"]) & app.sudoers)
async def userbot_leave_cmd(_, message: types.Message):
    if not userbot.clients:
        return await message.reply_text("❌ No active assistant clients found.", quote=True)

    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = message.command[1]

    msg = await message.reply_text(f"⚡ Leaving target chat with assistant...", quote=True)
    client = userbot.clients[0]
    try:
        await client.leave_chat(chat_id)
        await msg.edit_text(f"✅ Assistant successfully left <code>{chat_id}</code>!")
    except Exception as e:
        await msg.edit_text(f"❌ Failed to leave chat: {e}")
