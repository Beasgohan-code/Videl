# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Environment Variables & Configuration Inspector Plugin

from pyrogram import filters, types
from videl import app, config


def mask_secret(val: str, show_chars: int = 4) -> str:
    if not val:
        return "None"
    s = str(val)
    if len(s) <= show_chars * 2:
        return "***"
    return s[:show_chars] + "*" * (len(s) - show_chars * 2) + s[-show_chars:]


@app.on_message(filters.command(["config", "variables", "vars"]) & app.sudoers)
async def variables_cmd(_, message: types.Message):
    text = f"""⚙️ <b><u>{app.name} Active Configuration</u></b>

• <b>API_ID:</b> <code>{config.API_ID}</code>
• <b>BOT_NAME:</b> <code>{config.BOT_NAME}</code>
• <b>OWNER_ID:</b> <code>{config.OWNER_ID}</code>
• <b>LOGGER_ID:</b> <code>{config.LOGGER_ID}</code>

<b><u>Limits & Rules:</u></b>
• <b>DURATION_LIMIT:</b> <code>{config.DURATION_LIMIT} min</code>
• <b>QUEUE_LIMIT:</b> <code>{config.QUEUE_LIMIT} tracks</code>
• <b>PLAYLIST_LIMIT:</b> <code>{config.PLAYLIST_LIMIT} tracks</code>
• <b>AUTO_LEAVE:</b> <code>{config.AUTO_LEAVE}</code>
• <b>AUTO_END:</b> <code>{config.AUTO_END}</code>
• <b>THUMB_GEN:</b> <code>{config.THUMB_GEN}</code>

<b><u>Channels & Support:</u></b>
• <b>SUPPORT_CHAT:</b> {config.SUPPORT_CHAT}
• <b>SUPPORT_CHANNEL:</b> {config.SUPPORT_CHANNEL}
• <b>GITHUB_REPO:</b> {config.GITHUB_REPO}

<b><u>Security Status:</u></b>
• <b>BOT_TOKEN:</b> <code>{mask_secret(config.BOT_TOKEN)}</code>
• <b>MONGO_URL:</b> <code>{mask_secret(config.MONGO_URL)}</code>
• <b>SESSION1:</b> <code>{'Configured' if config.SESSION1 else 'Missing'}</code>
• <b>SESSION2:</b> <code>{'Configured' if config.SESSION2 else 'Not Set'}</code>
• <b>SESSION3:</b> <code>{'Configured' if config.SESSION3 else 'Not Set'}</code>
• <b>SESSION4:</b> <code>{'Configured' if config.SESSION4 else 'Not Set'}</code>
• <b>SESSION5:</b> <code>{'Configured' if config.SESSION5 else 'Not Set'}</code>
"""

    if message.chat.type == types.enums.ChatType.PRIVATE:
        await message.reply_text(text, quote=True, disable_web_page_preview=True)
    else:
        try:
            await app.send_message(message.from_user.id, text, disable_web_page_preview=True)
            await message.reply_text("📩 Sent active configuration to your PM for security.", quote=True)
        except Exception:
            await message.reply_text("❌ Please start the bot in PM first to receive configuration variables.", quote=True)
