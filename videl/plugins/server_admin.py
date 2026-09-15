# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot Admin & Server Management Plugin

import os
import sys
import psutil
import platform
import asyncio
import importlib
from pyrogram import filters, types
from videl import app, db, config, logger
from videl.plugins import all_modules


@app.on_message(filters.command(["sysinfo", "hostinfo"]) & app.sudoers)
async def sysinfo_cmd(_, message: types.Message):
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    cpu_percent = psutil.cpu_percent(interval=0.5)

    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")

    text = f"""🖥 <b><u>System & Host Diagnostics</u></b>

⚙️ <b><u>Processor & Architecture:</u></b>
• <b>OS:</b> <code>{platform.system()} {platform.release()}</code>
• <b>Arch:</b> <code>{platform.machine()}</code>
• <b>CPU Cores:</b> <code>{cpu_count}</code>
• <b>CPU Frequency:</b> <code>{cpu_freq:.0f} MHz</code>
• <b>CPU Usage:</b> <code>{cpu_percent}%</code>

📊 <b><u>Memory & Storage:</u></b>
• <b>RAM Used:</b> <code>{mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB ({mem.percent}%)</code>
• <b>RAM Available:</b> <code>{mem.available / (1024**3):.2f} GB</code>
• <b>Swap Used:</b> <code>{swap.used / (1024**3):.2f} GB / {swap.total / (1024**3):.2f} GB ({swap.percent}%)</code>
• <b>Disk Usage:</b> <code>{disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB ({disk.percent}%)</code>

🐍 <b><u>Software Runtime:</u></b>
• <b>Python:</b> <code>{platform.python_version()}</code>
• <b>Pyrogram:</b> <code>2.0+</code>
• <b>PyTgCalls:</b> <code>2.3+</code>
• <b>MongoDB:</b> <code>Connected</code>
"""
    await message.reply_text(text, quote=True)


@app.on_message(filters.command(["servedchats", "chatlist"]) & app.sudoers)
async def served_chats_export(_, message: types.Message):
    msg = await message.reply_text("⚡ Exporting list of served chats...", quote=True)
    chats = await db.get_chats()

    file_path = "served_chats.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"=== {app.name} Served Chats ({len(chats)}) ===\n\n")
        for cid in chats:
            f.write(f"{cid}\n")

    await message.reply_document(
        document=file_path,
        caption=f"📁 <b>Served Chats Export:</b> <code>{len(chats)}</code> chats total.",
        quote=True,
    )
    if os.path.exists(file_path):
        os.remove(file_path)
    await msg.delete()


@app.on_message(filters.command(["servedusers", "userlist"]) & app.sudoers)
async def served_users_export(_, message: types.Message):
    msg = await message.reply_text("⚡ Exporting list of served users...", quote=True)
    users = await db.get_users()

    file_path = "served_users.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"=== {app.name} Served Users ({len(users)}) ===\n\n")
        for uid in users:
            f.write(f"{uid}\n")

    await message.reply_document(
        document=file_path,
        caption=f"📁 <b>Served Users Export:</b> <code>{len(users)}</code> users total.",
        quote=True,
    )
    if os.path.exists(file_path):
        os.remove(file_path)
    await msg.delete()


@app.on_message(filters.command(["botleave", "leavechat"]) & app.sudoers)
async def bot_leave_cmd(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: <code>/botleave [chat_id]</code>", quote=True)

    try:
        chat_id = int(message.command[1])
        await app.leave_chat(chat_id)
        await message.reply_text(f"✅ Bot successfully left chat <code>{chat_id}</code>.", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Failed to leave chat: {e}", quote=True)


@app.on_message(filters.command(["logger"]) & app.sudoers)
async def logger_toggle_cmd(_, message: types.Message):
    if len(message.command) < 2 or message.command[1].lower() not in ("on", "off"):
        status = await db.is_logger()
        return await message.reply_text(
            f"📝 <b>Channel Logger Status:</b> <code>{'Enabled' if status else 'Disabled'}</code>\n\n"
            "Use <code>/logger on</code> or <code>/logger off</code> to toggle error logging to LOGGER_ID.",
            quote=True,
        )

    enable = message.command[1].lower() == "on"
    await db.set_logger(enable)
    await message.reply_text(f"📝 <b>Channel Logger is now:</b> <code>{'Enabled' if enable else 'Disabled'}</code>", quote=True)


@app.on_message(filters.command(["announce", "vcannounce"]) & app.sudoers)
async def announce_cmd(_, message: types.Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("❌ Please specify announcement text or reply to a message.", quote=True)

    text = message.reply_to_message.text if message.reply_to_message else message.text.split(None, 1)[1]
    active_chats = list(db.active_calls.keys())

    if not active_chats:
        return await message.reply_text("❌ No active voice chat calls currently streaming.", quote=True)

    msg = await message.reply_text(f"📢 <b>Broadcasting announcement to {len(active_chats)} active voice chats...</b>", quote=True)
    sent_count = 0

    for chat_id in active_chats:
        try:
            sent_msg = await app.send_message(
                chat_id,
                f"📢 <b><u>Bot Announcement</u></b>\n\n{text}",
            )
            try:
                await sent_msg.pin(disable_notification=False)
            except Exception:
                pass
            sent_count += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass

    await msg.edit_text(f"✅ Announcement sent to <b>{sent_count}</b> active voice chat(s)!")


@app.on_message(filters.command(["reloadplugins", "hotreload"]) & app.sudoers)
async def reload_plugins_cmd(_, message: types.Message):
    msg = await message.reply_text("⚡ Reloading all plugins...", quote=True)
    reloaded = 0
    errors = 0

    for module in all_modules:
        try:
            mod = importlib.import_module(f"videl.plugins.{module}")
            importlib.reload(mod)
            reloaded += 1
        except Exception as e:
            errors += 1
            logger.error(f"Failed to reload plugin {module}: {e}")

    await msg.edit_text(f"✅ Successfully reloaded <b>{reloaded}</b> plugins! (Errors: {errors})")
