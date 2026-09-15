# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Play Middleware & Assistant Auto-Join Handler

import asyncio
from functools import wraps
from pyrogram import enums, errors, types
from videl import app, config, db, logger, queue, yt
from videl.helpers._utilities import get_url


def checkUB(play_func):
    @wraps(play_func)
    async def wrapper(client, m: types.Message):
        if not m.from_user:
            return await m.reply_text(m.lang["play_user_invalid"])

        chat_id = m.chat.id
        if m.chat.type != enums.ChatType.SUPERGROUP:
            try:
                await m.reply_text(m.lang["play_chat_invalid"])
                return await app.leave_chat(chat_id)
            except Exception:
                return

        if not m.reply_to_message and (
            len(m.command) < 2 or (len(m.command) == 2 and m.command[1] == "-f")
        ):
            return await m.reply_text(m.lang["play_usage"])

        if len(queue.get_queue(chat_id)) >= config.QUEUE_LIMIT:
            return await m.reply_text(m.lang["play_queue_full"].format(config.QUEUE_LIMIT))

        force = m.command[0].endswith("force") or (
            len(m.command) > 1 and "-f" in m.command[1]
        )
        video = m.command[0][0] == "v" and config.VIDEO_PLAY
        url = get_url(m)
        if url and yt.invalid(url):
            return await m.reply_text(m.lang["play_not_found"].format(config.SUPPORT_CHAT))
        m3u8 = bool(url and not yt.valid(url))

        play_mode = await db.get_play_mode(chat_id)
        if play_mode or force:
            adminlist = await db.get_admins(chat_id)
            if (
                m.from_user.id not in adminlist
                and not await db.is_auth(chat_id, m.from_user.id)
                and m.from_user.id not in app.sudoers
            ):
                return await m.reply_text(m.lang["play_admin"])

        if chat_id not in db.active_calls:
            assistant = await db.get_client(chat_id)
            try:
                member = await app.get_chat_member(chat_id, assistant.id)
                if member.status in (
                    enums.ChatMemberStatus.BANNED,
                    enums.ChatMemberStatus.RESTRICTED,
                ):
                    try:
                        await app.unban_chat_member(chat_id=chat_id, user_id=assistant.id)
                    except Exception:
                        return await m.reply_text(
                            m.lang["play_banned"].format(
                                app.name,
                                assistant.id,
                                assistant.mention,
                                f"@{assistant.username}" if assistant.username else "",
                            )
                        )
            except errors.ChatAdminRequired:
                return await m.reply_text(m.lang["admin_required"])
            except (errors.UserNotParticipant, errors.exceptions.bad_request_400.UserNotParticipant):
                if m.chat.username:
                    invite_link = m.chat.username
                    try:
                        await assistant.resolve_peer(invite_link)
                    except Exception:
                        pass
                else:
                    try:
                        chat_obj = await app.get_chat(chat_id)
                        invite_link = chat_obj.invite_link or await app.export_chat_invite_link(chat_id)
                    except errors.ChatAdminRequired:
                        return await m.reply_text(m.lang["admin_required"])
                    except Exception as ex:
                        return await m.reply_text(
                            m.lang["play_invite_error"].format(type(ex).__name__)
                        )

                join_msg = await m.reply_text(m.lang["play_invite"].format(app.name))
                await asyncio.sleep(1)
                try:
                    await assistant.join_chat(invite_link)
                except errors.UserAlreadyParticipant:
                    pass
                except errors.InviteRequestSent:
                    await asyncio.sleep(1)
                    try:
                        await app.approve_chat_join_request(chat_id, assistant.id)
                    except Exception:
                        pass
                except Exception as ex:
                    logger.error(f"Assistant error joining chat {chat_id}: {ex}")
                    return await join_msg.edit_text(
                        m.lang["play_invite_error"].format(type(ex).__name__)
                    )

                try:
                    await join_msg.delete()
                    await assistant.resolve_peer(chat_id)
                except Exception:
                    pass

        if await db.get_cmd_delete(chat_id):
            try:
                await m.delete()
            except Exception:
                pass

        return await play_func(client, m, force, m3u8, video, url)

    return wrapper
