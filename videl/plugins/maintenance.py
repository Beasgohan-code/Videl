# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Maintenance Mode, Assistant Health & DB Backup Plugin

import json
import os
from pyrogram import filters, types
from videl import anon, app, config, db, userbot


@app.on_message(filters.command(["maintenance", "maintenancemode"]) & filters.user(app.owner))
async def maintenance_toggle(_, message: types.Message):
    if len(message.command) < 2 or message.command[1].lower() not in ("on", "off"):
        status = await db.get_maintenance()
        return await message.reply_text(
            f"🛠 <b>Maintenance Mode:</b> <code>{'Enabled' if status else 'Disabled'}</code>\n\n"
            "Use <code>/maintenance on</code> or <code>/maintenance off</code> to toggle.",
            quote=True,
        )

    enable = message.command[1].lower() == "on"
    await db.set_maintenance(enable)
    await message.reply_text(f"🛠 <b>Maintenance Mode is now {'Enabled' if enable else 'Disabled'}.</b>", quote=True)


@app.on_message(filters.command(["assistants", "checksessions", "ubstats"]) & app.sudoers)
async def assistants_status(_, message: types.Message):
    sent = await message.reply_text("⚡ <i>Checking assistant accounts health...</i>")
    text = f"🤖 <b><u>Videl Assistant Cluster Status</u></b>\n\n<blockquote expandable>"

    if not userbot.clients:
        text += "❌ No active assistant accounts booted.\n"
    else:
        for idx, client in enumerate(userbot.clients, 1):
            status = "🟢 Online" if client.is_connected else "🔴 Offline"
            asst_ping = round(anon.clients[idx - 1].ping, 2) if idx - 1 < len(anon.clients) else 0.0
            text += (
                f"<b>Assistant #{idx}:</b>\n"
                f"• <b>Name:</b> {client.name}\n"
                f"• <b>Username:</b> @{client.username if client.username else 'None'}\n"
                f"• <b>ID:</b> <code>{client.id}</code>\n"
                f"• <b>Status:</b> <code>{status}</code>\n"
                f"• <b>PyTgCalls Ping:</b> <code>{asst_ping}ms</code>\n\n"
            )

    text += f"📊 <b>Total Cluster Assistants:</b> <code>{len(userbot.clients)} / 5</code>\n"
    text += f"📞 <b>Active Stream Calls:</b> <code>{len(db.active_calls)}</code>\n"
    text += "</blockquote>"

    await sent.edit_text(text)


@app.on_message(filters.command(["dbbackup", "backupdb"]) & filters.user(app.owner))
async def db_backup_cmd(_, message: types.Message):
    sent = await message.reply_text("📦 <i>Exporting database collections...</i>")

    backup_data = {
        "chats": await db.get_chats(),
        "users": await db.get_users(),
        "sudoers": await db.get_sudoers(),
        "blacklisted": await db.get_blacklisted(),
        "exported_at": str(os.getenv("CURRENT_TIME", "2026-09-15")),
    }

    os.makedirs("downloads", exist_ok=True)
    out_path = "downloads/videl_database_backup.json"

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2)

        caption = (
            f"📦 <b><u>Videl MongoDB Backup Archive</u></b>\n\n"
            f"• <b>Chats:</b> <code>{len(backup_data['chats'])}</code>\n"
            f"• <b>Users:</b> <code>{len(backup_data['users'])}</code>\n"
            f"• <b>Sudoers:</b> <code>{len(backup_data['sudoers'])}</code>"
        )
        await message.reply_document(document=out_path, caption=caption, quote=True)
        await sent.delete()
    except Exception as ex:
        await sent.edit_text(f"❌ <b>Backup error:</b> <code>{ex}</code>")
    finally:
        if os.path.exists(out_path):
            os.remove(out_path)
