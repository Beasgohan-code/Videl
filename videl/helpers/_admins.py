# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Admin Permissions & Role Checker

from functools import wraps
from pyrogram import enums, types, StopPropagation


def admin_check(func):
    """Ensure user is an administrator or bot sudoer."""
    @wraps(func)
    async def wrapper(client, update: types.Message | types.CallbackQuery, *args, **kwargs):
        from videl import app, db

        async def reply(text):
            if isinstance(update, types.Message):
                return await update.reply_text(text)
            else:
                return await update.answer(text, show_alert=True)

        chat = update.chat if isinstance(update, types.Message) else update.message.chat
        if chat.type == enums.ChatType.PRIVATE:
            return await func(client, update, *args, **kwargs)

        user_id = update.from_user.id
        if user_id in app.sudoers:
            return await func(client, update, *args, **kwargs)

        admins = await db.get_admins(chat.id)
        if user_id not in admins:
            return await reply(update.lang["user_no_perms"])

        return await func(client, update, *args, **kwargs)

    return wrapper


def can_manage_vc(func):
    """Ensure user can manage voice chat (admin, auth user, or sudoer)."""
    @wraps(func)
    async def wrapper(client, update: types.Message | types.CallbackQuery, *args, **kwargs):
        from videl import app, db

        chat_id = update.chat.id if isinstance(update, types.Message) else update.message.chat.id
        user_id = update.from_user.id

        if user_id in app.sudoers:
            return await func(client, update, *args, **kwargs)

        if await db.is_auth(chat_id, user_id):
            return await func(client, update, *args, **kwargs)

        admins = await db.get_admins(chat_id)
        if user_id in admins:
            return await func(client, update, *args, **kwargs)

        if isinstance(update, types.Message):
            return await update.reply_text(update.lang["user_no_perms"])
        else:
            return await update.answer(update.lang["user_no_perms"], show_alert=True)

    return wrapper


async def is_admin(chat_id: int, user_id: int) -> bool:
    from videl import app, db
    if user_id in await db.get_admins(chat_id):
        return True
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER,
        )
    except Exception:
        raise StopPropagation


async def reload_admins(chat_id: int) -> list[int]:
    from videl import app
    try:
        admins = [
            admin
            async for admin in app.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
            if not admin.user.is_bot
        ]
        return [admin.user.id for admin in admins]
    except Exception:
        return []
