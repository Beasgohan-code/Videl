# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Text-to-Speech & Voice Synthesizer Plugin

import os
import asyncio
from pyrogram import filters, types
from videl import app

try:
    from gtts import gTTS
except ImportError:
    gTTS = None


@app.on_message(filters.command(["tts", "voice"]) & ~app.bl_users)
async def tts_handler(_, message: types.Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("<b>Usage:</b> <code>/tts [text]</code> or <code>/tts [lang_code] [text]</code> (e.g. <code>/tts hi नमस्ते</code>)", quote=True)

    if not gTTS:
        return await message.reply_text("❌ gTTS library not available.")

    lang_code = "en"
    text = ""

    if len(message.command) > 2 and len(message.command[1]) == 2:
        lang_code = message.command[1].lower()
        text = " ".join(message.command[2:])
    elif len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption or ""

    if not text:
        return await message.reply_text("Please provide some text to synthesize.")

    os.makedirs("downloads", exist_ok=True)
    out_file = f"downloads/tts_{message.id}.mp3"

    try:
        def _synth():
            tts = gTTS(text=text[:500], lang=lang_code)
            tts.save(out_file)

        await asyncio.to_thread(_synth)
        await message.reply_voice(voice=out_file, caption=f"🗣 <i>Language: <code>{lang_code}</code></i>", quote=True)
    except Exception as ex:
        await message.reply_text(f"❌ <b>TTS synthesis failed:</b> <code>{ex}</code>", quote=True)
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)
