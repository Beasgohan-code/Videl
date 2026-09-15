# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Assistant Real-Time Auto-Bio Sync Plugin

import asyncio
from pyrogram import filters, types
from videl import app, db, queue, userbot

autobio_enabled = False


async def bio_sync_loop():
    """Background task to sync assistants' profile bio with currently playing track."""
    while True:
        await asyncio.sleep(60)
        if not autobio_enabled or not userbot.clients:
            continue

        active = list(db.active_calls.keys())
        if active:
            first_chat = active[0]
            media = queue.get_current(first_chat)
            if media:
                bio_text = f"⚡ Streaming: {media.title[:45]} | @{app.username}"
            else:
                bio_text = f"✨ Videl Assistant | @{app.username}"
        else:
            bio_text = f"⚡ High-Speed Voice Chat Assistant | @{app.username}"

        for ub in userbot.clients:
            try:
                await ub.update_profile(bio=bio_text[:70])
            except Exception:
                pass


@app.on_message(filters.command(["autobio"]) & app.sudoers)
async def autobio_toggle(_, message: types.Message):
    global autobio_enabled
    if len(message.command) < 2 or message.command[1].lower() not in ("on", "off"):
        return await message.reply_text(
            f"⚡ <b>Assistant Auto-Bio Sync:</b> <code>{'Enabled' if autobio_enabled else 'Disabled'}</code>\n\n"
            "Use <code>/autobio on</code> or <code>/autobio off</code> to toggle automatic profile bio updates with currently streaming music.",
            quote=True,
        )

    autobio_enabled = message.command[1].lower() == "on"
    await message.reply_text(f"⚡ <b>Assistant Auto-Bio Sync is now:</b> <code>{'Enabled' if autobio_enabled else 'Disabled'}</code>", quote=True)


def init_autobio():
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(bio_sync_loop())
    except RuntimeError:
        pass


init_autobio()

