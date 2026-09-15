# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Speedtest & Network Diagnostics Plugin

import asyncio
from pyrogram import filters, types
from videl import app

try:
    import speedtest
except ImportError:
    speedtest = None


def run_speedtest():
    if not speedtest:
        return None
    st = speedtest.Speedtest()
    st.get_best_server()
    st.download()
    st.upload()
    st.results.share()
    return st.results.dict()


@app.on_message(filters.command(["speedtest", "spt"]) & app.sudoers)
async def speedtest_cmd(_, message: types.Message):
    m = await message.reply_text("⚡ <i>Running network speedtest...</i>")
    try:
        results = await asyncio.to_thread(run_speedtest)
        if not results:
            return await m.edit_text("❌ Speedtest module not available.")

        caption = (
            f"🚀 <b><u>Videl Network Speedtest</u></b>\n\n"
            f"<b>Client:</b>\n"
            f"• <b>ISP:</b> <code>{results['client']['isp']}</code>\n"
            f"• <b>Country:</b> <code>{results['client']['country']}</code>\n\n"
            f"<b>Server:</b>\n"
            f"• <b>Name:</b> <code>{results['server']['name']}</code> ({results['server']['country']})\n"
            f"• <b>Sponsor:</b> <code>{results['server']['sponsor']}</code>\n"
            f"• <b>Latency:</b> <code>{results['server']['latency']:.2f} ms</code>\n\n"
            f"<b>Speed:</b>\n"
            f"• <b>Download:</b> <code>{results['download'] / 1024 / 1024:.2f} Mbps</code>\n"
            f"• <b>Upload:</b> <code>{results['upload'] / 1024 / 1024:.2f} Mbps</code>\n"
            f"• <b>Ping:</b> <code>{results['ping']} ms</code>"
        )

        share_img = results.get("share")
        if share_img:
            await app.send_photo(chat_id=message.chat.id, photo=share_img, caption=caption)
            await m.delete()
        else:
            await m.edit_text(caption)
    except Exception as ex:
        await m.edit_text(f"❌ <b>Speedtest error:</b> <code>{ex}</code>")
