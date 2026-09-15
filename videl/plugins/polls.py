# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Bot API Interactive Polls & Quiz System

from pyrogram import filters, types
from videl import app, bridge


@app.on_message(filters.command(["poll", "vote"]) & ~app.bl_users)
async def poll_handler(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "📊 <b><u>Interactive Poll Creator</u></b>\n\n"
            "<b>Usage:</b> <code>/poll Question /// Option 1 /// Option 2 /// Option 3</code>\n"
            "<i>Example:</i> <code>/poll Best Music Genre? /// EDM /// Hip-Hop /// Rock /// Lofi</code>",
            quote=True,
        )

    raw_text = message.text.split(None, 1)[1]
    parts = [p.strip() for p in raw_text.split("///") if p.strip()]

    if len(parts) < 3:
        return await message.reply_text("❌ A poll requires a question and at least 2 options separated by <code>///</code>.", quote=True)

    question = parts[0]
    options = parts[1:11]  # Max 10 options

    await bridge.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        allows_multiple_answers=False,
    )


@app.on_message(filters.command(["quiz", "musicpoll"]) & ~app.bl_users)
async def quiz_handler(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "🧠 <b><u>Interactive Quiz Creator</u></b>\n\n"
            "<b>Usage:</b> <code>/quiz Question /// Option 1 /// Correct Option* /// Option 3</code>\n"
            "<i>Note: Put an asterisk <code>*</code> next to the correct answer!</i>\n\n"
            "<i>Example:</i> <code>/quiz Who sang 'Shape of You'? /// Bruno Mars /// Ed Sheeran* /// The Weeknd</code>",
            quote=True,
        )

    raw_text = message.text.split(None, 1)[1]
    parts = [p.strip() for p in raw_text.split("///") if p.strip()]

    if len(parts) < 3:
        return await message.reply_text("❌ A quiz requires a question and at least 2 options separated by <code>///</code>.", quote=True)

    question = parts[0]
    raw_options = parts[1:11]

    correct_idx = 0
    clean_options = []

    for i, opt in enumerate(raw_options):
        if opt.endswith("*") or opt.startswith("*"):
            correct_idx = i
            clean_options.append(opt.replace("*", "").strip())
        else:
            clean_options.append(opt)

    await bridge.send_quiz(
        chat_id=message.chat.id,
        question=question,
        options=clean_options,
        correct_option_id=correct_idx,
        explanation=f"Correct Answer: {clean_options[correct_idx]} 🎵",
    )
