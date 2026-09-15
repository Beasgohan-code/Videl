# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Cache & Disk Cleaner Plugin

import os
import time
import asyncio
from pyrogram import filters, types
from videl import app, logger


def remove_stale_files(max_age_seconds: int = 3600) -> int:
    deleted = 0
    now = time.time()
    target_dirs = ["downloads", "cache"]

    for d in target_dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    if now - os.path.getmtime(filepath) > max_age_seconds:
                        os.remove(filepath)
                        deleted += 1
                except Exception:
                    pass
    return deleted


async def auto_clean_task():
    while True:
        await asyncio.sleep(1800)  # Every 30 minutes
        try:
            cleaned = remove_stale_files(max_age_seconds=1800)
            if cleaned > 0:
                logger.info(f"Garbage collector purged {cleaned} stale temporary download file(s).")
        except Exception:
            pass


def init_cleaner():
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(auto_clean_task())
    except RuntimeError:
        pass


init_cleaner()


@app.on_message(filters.command(["clearcache", "cleanup", "rmdownloads"]) & app.sudoers)
async def clean_cache_cmd(_, message: types.Message):
    msg = await message.reply_text("🧹 Purging temporary media, cache, and downloads...", quote=True)
    deleted = remove_stale_files(max_age_seconds=0)  # Purge all temp files immediately
    await msg.edit_text(f"✅ Disk cleanup complete! Purged <b>{deleted}</b> cached file(s).")
