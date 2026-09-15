# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Developer Eval & Terminal Plugin

import io
import os
import re
import sys
import uuid
import asyncio
import traceback
from html import escape
from typing import Any, Optional, Tuple
from pyrogram import filters, types
from videl import anon, app, config, db, lang, queue, userbot
from videl.helpers._exec import format_exception, meval


@app.on_message(filters.command(["eval", "exec"]) & filters.user(app.owner))
@app.on_edited_message(filters.command(["eval", "exec"]) & filters.user(app.owner))
@lang.language()
async def eval_handler(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text(message.lang["eval_inp"])

    code = message.text.split(None, 1)[1]
    out_buf = io.StringIO()

    async def _eval_code() -> Tuple[str, Optional[str]]:
        async def send(*args: Any, **kwargs: Any) -> types.Message:
            return await message.reply_text(*args, **kwargs)

        def _print(*args: Any, **kwargs: Any) -> None:
            kwargs.setdefault("file", out_buf)
            print(*args, **kwargs)

        eval_vars = {
            "m": message,
            "r": message.reply_to_message,
            "chat": message.chat,
            "user": message.from_user,
            "app": app,
            "anon": anon,
            "db": db,
            "queue": queue,
            "client": app,
            "ub": userbot,
            "ikb": types.InlineKeyboardButton,
            "ikm": types.InlineKeyboardMarkup,
            "send": send,
            "config": config,
            "print": _print,
            "os": os,
            "re": re,
            "sys": sys,
            "tb": traceback,
        }

        try:
            result = await meval(code, globals(), **eval_vars)
            return "", result
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            snippet_tb = next(
                (i for i, f in enumerate(tb) if f.filename == "<string>"), -1
            )
            formatted_tb = format_exception(
                e, tb[snippet_tb:] if snippet_tb != -1 else tb
            )
            return message.lang["eval_error"], formatted_tb

    _, result = await _eval_code()

    if result is not None or not out_buf.getvalue():
        print(result, file=out_buf)

    output = out_buf.getvalue().strip()
    response = message.lang["eval_out"].format(escape(output))

    if len(response) > 4096:
        with io.BytesIO(output.encode()) as out_file:
            out_file.name = f"eval_{uuid.uuid4().hex[:6]}.txt"
            return await message.reply_document(document=out_file, disable_notification=True)

    await message.reply_text(response)


@app.on_message(filters.command(["sh", "bash", "shell"]) & filters.user(app.owner))
async def sh_handler(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/sh command</code>")

    cmd = message.text.split(None, 1)[1]
    msg = await message.reply_text("⚙️ <i>Executing bash command...</i>")
    
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    result = (stdout.decode() + stderr.decode()).strip()

    if not result:
        result = "No output."

    if len(result) > 4096:
        with io.BytesIO(result.encode()) as out_file:
            out_file.name = "output.txt"
            await message.reply_document(document=out_file)
            await msg.delete()
    else:
        await msg.edit_text(f"<b>Output:</b>\n<pre><code>{escape(result)}</code></pre>")
