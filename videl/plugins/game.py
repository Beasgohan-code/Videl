# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Voice Chat Music Trivia Game Plugin

import asyncio
import random
from pyrogram import filters, types
from videl import anon, app, db, queue, yt
from videl.helpers._dataclass import Track
from videl.helpers.button_style import styled_button, ButtonStyle

QUIZ_SONGS = [
    {"title": "Shape of You", "query": "Ed Sheeran Shape of You", "artist": "Ed Sheeran"},
    {"title": "Blinding Lights", "query": "The Weeknd Blinding Lights", "artist": "The Weeknd"},
    {"title": "Believer", "query": "Imagine Dragons Believer", "artist": "Imagine Dragons"},
    {"title": "Faded", "query": "Alan Walker Faded", "artist": "Alan Walker"},
    {"title": "Bad Guy", "query": "Billie Eilish Bad Guy", "artist": "Billie Eilish"},
    {"title": "Despacito", "query": "Luis Fonsi Despacito", "artist": "Luis Fonsi"},
    {"title": "Stay", "query": "The Kid LAROI Justin Bieber Stay", "artist": "Justin Bieber"},
    {"title": "Starboy", "query": "The Weeknd Starboy", "artist": "The Weeknd"},
    {"title": "Counting Stars", "query": "OneRepublic Counting Stars", "artist": "OneRepublic"},
    {"title": "Levitating", "query": "Dua Lipa Levitating", "artist": "Dua Lipa"},
]

active_quizzes = {}


@app.on_message(filters.command(["songquiz", "guessthesong", "musicquiz"]) & filters.group & ~app.bl_users)
async def start_quiz(_, message: types.Message):
    chat_id = message.chat.id
    if chat_id in active_quizzes:
        return await message.reply_text("🎮 <b>A music quiz is already active in this group!</b>")

    chosen = random.choice(QUIZ_SONGS)
    active_quizzes[chat_id] = {
        "title": chosen["title"].lower(),
        "artist": chosen["artist"].lower(),
        "display": chosen["title"],
    }

    sent = await message.reply_text(
        "🎮 <b><u>Voice Chat Song Trivia Quiz!</u></b>\n\n"
        "⚡ <i>Streaming mystery track into voice chat...</i>\n"
        "Guess the song title or artist in this chat within <b>45 seconds</b>!",
    )

    track = await yt.search(chosen["query"], message.id)
    if track:
        track.user = "Music Quiz"
        track.file_path = await yt.download(track.id)
        queue.clear(chat_id)
        queue.add(chat_id, track)
        await anon.play_media(chat_id, sent, track, seek_time=30)

    # Timer wait loop
    await asyncio.sleep(45)

    if chat_id in active_quizzes:
        ans = active_quizzes.pop(chat_id)
        await app.send_message(
            chat_id=chat_id,
            text=f"⏰ <b>Time's Up!</b> Nobody guessed it.\n\n🎵 <b>The song was:</b> <i>{ans['display']}</i>",
        )


@app.on_message(filters.group & ~filters.me, group=16)
async def quiz_answer_checker(_, message: types.Message):
    chat_id = message.chat.id
    if chat_id not in active_quizzes or not message.text:
        return

    ans = active_quizzes[chat_id]
    text = message.text.lower().strip()

    if ans["title"] in text or ans["artist"] in text:
        active_quizzes.pop(chat_id)
        await message.reply_text(
            f"🎉 <b>BINGO! Correct answer!</b>\n\n"
            f"🏆 {message.from_user.mention} <b>guessed the song correctly:</b> <i>{ans['display']}</i>!",
            quote=True,
        )
