# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Sudo Users Management Plugin

from pyrogram import filters, types
from videl import app, db, lang
from videl.helpers._utilities import extract_user

o_mention = None


@app.on_message(filters.command(["addsudo", "delsudo", "rmsudo"]) & filters.user(app.owner))
@lang.language()
async def _sudo(_, m: types.Message):
    user = await extract_user(m)
    if not user:
        return await m.reply_text(m.lang["user_not_found"])

    if m.command[0] == "addsudo":
        if user.id in app.sudoers:
            return await m.reply_text(m.lang["sudo_already"].format(user.mention))

        app.sudoers.add(user.id)
        await db.add_sudo(user.id)
        await m.reply_text(m.lang["sudo_added"].format(user.mention))
    else:
        if user.id not in app.sudoers:
            return await m.reply_text(m.lang["sudo_not"].format(user.mention))

        app.sudoers.discard(user.id)
        await db.del_sudo(user.id)
        await m.reply_text(m.lang["sudo_removed"].format(user.mention))


@app.on_message(filters.command(["listsudo", "sudolist"]))
@lang.language()
async def _listsudo(_, m: types.Message):
    global o_mention
    sent = await m.reply_text(m.lang["sudo_fetching"])

    if not o_mention:
        try:
            o_mention = (await app.get_users(app.owner)).mention
        except Exception:
            o_mention = f"<code>{app.owner}</code>"

    txt = m.lang["sudo_owner"].format(o_mention)
    sudoers = await db.get_sudoers()
    if sudoers:
        txt += m.lang["sudo_users"]

    for user_id in sudoers:
        try:
            user = (await app.get_users(user_id)).mention
            txt += f"\n- {user}"
        except Exception:
            txt += f"\n- <code>{user_id}</code>"

    await sent.edit_text(txt)
