# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl In-Bot Interactive String Session Generator (Admin Only)

import asyncio
from pyrogram import Client, filters, types
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from videl import app, config

# Memory state dict: user_id -> state dict
SESSION_STATES = {}


@app.on_message(filters.command(["generate_session", "genstring", "sessiongen"]) & filters.private & app.sudoers)
async def gen_session_start(_, message: types.Message):
    user_id = message.from_user.id
    if user_id in SESSION_STATES:
        old_client = SESSION_STATES[user_id].get("client")
        if old_client:
            try:
                await old_client.disconnect()
            except Exception:
                pass
        SESSION_STATES.pop(user_id, None)

    SESSION_STATES[user_id] = {
        "step": "phone",
        "api_id": config.API_ID,
        "api_hash": config.API_HASH,
        "client": None,
        "phone": None,
        "phone_code_hash": None,
    }

    await message.reply_text(
        "🔐 <b><u>Videl String Session Generator (Admin Only)</u></b>\n\n"
        f"Using configured API ID: <code>{config.API_ID}</code>\n\n"
        "Please send your <b>Phone Number</b> with country code.\n"
        "<i>Example:</i> <code>+12345678900</code>\n\n"
        "Type <code>/cancel</code> at any time to abort.",
        quote=True,
    )


@app.on_message(filters.command(["cancel"]) & filters.private & app.sudoers)
async def gen_session_cancel(_, message: types.Message):
    user_id = message.from_user.id
    if user_id in SESSION_STATES:
        client = SESSION_STATES[user_id].get("client")
        if client:
            try:
                await client.disconnect()
            except Exception:
                pass
        SESSION_STATES.pop(user_id, None)
        return await message.reply_text("✅ Session generation cancelled.", quote=True)
    await message.reply_text("❌ No active session generation in progress.", quote=True)


@app.on_message(filters.private & ~filters.command(["generate_session", "genstring", "sessiongen", "cancel"]) & app.sudoers)
async def gen_session_flow(_, message: types.Message):
    user_id = message.from_user.id
    if user_id not in SESSION_STATES:
        return

    state = SESSION_STATES[user_id]
    step = state["step"]

    # Step 1: Handle Phone Number
    if step == "phone":
        phone_number = message.text.strip().replace(" ", "")
        state["phone"] = phone_number

        temp_client = Client(
            name=f"temp_session_{user_id}",
            api_id=state["api_id"],
            api_hash=state["api_hash"],
            in_memory=True,
        )
        state["client"] = temp_client

        try:
            await temp_client.connect()
            sent_code = await temp_client.send_code(phone_number)
            state["phone_code_hash"] = sent_code.phone_code_hash
            state["step"] = "code"

            await message.reply_text(
                "📩 <b>OTP Sent via Telegram!</b>\n\n"
                "Please enter the login code you received from Telegram.\n"
                "<i>Note: You can format the code with spaces if needed (e.g., <code>1 2 3 4 5</code>) to bypass filters.</i>",
                quote=True,
            )
        except ApiIdInvalid:
            await message.reply_text("❌ Invalid API ID or API Hash. Aborting.")
            SESSION_STATES.pop(user_id, None)
        except PhoneNumberInvalid:
            await message.reply_text("❌ Invalid Phone Number format. Please try again with country code e.g. <code>+12345678900</code>:")
        except Exception as e:
            await message.reply_text(f"❌ Error sending OTP: {e}\nAborted.")
            SESSION_STATES.pop(user_id, None)

    # Step 2: Handle Verification Code
    elif step == "code":
        raw_code = message.text.strip().replace(" ", "").replace("-", "")
        client: Client = state["client"]

        try:
            await client.sign_in(
                phone_number=state["phone"],
                phone_code_hash=state["phone_code_hash"],
                phone_code=raw_code,
            )

            # Successfully signed in without 2FA
            session_str = await client.export_session_string()
            await client.disconnect()
            SESSION_STATES.pop(user_id, None)

            await message.reply_text(
                "🎉 <b><u>Your String Session is Ready!</u></b>\n\n"
                f"<code>{session_str}</code>\n\n"
                "⚠️ <b>WARNING:</b> Never share this string session with anyone! Anyone with this string can access your Telegram account.",
                quote=True,
            )
        except SessionPasswordNeeded:
            state["step"] = "password"
            await message.reply_text(
                "🔐 <b>Two-Factor Authentication (2FA) Detected!</b>\n\n"
                "Please enter your Telegram Two-Step Verification cloud password:",
                quote=True,
            )
        except (PhoneCodeInvalid, PhoneCodeExpired) as ex:
            await message.reply_text(f"❌ Invalid or expired code: {ex}. Please re-enter the code:")
        except Exception as e:
            await message.reply_text(f"❌ Error signing in: {e}\nSession generation aborted.")
            if client:
                try:
                    await client.disconnect()
                except Exception:
                    pass
            SESSION_STATES.pop(user_id, None)

    # Step 3: Handle 2FA Password
    elif step == "password":
        password = message.text.strip()
        client: Client = state["client"]

        try:
            await client.check_password(password=password)
            session_str = await client.export_session_string()
            await client.disconnect()
            SESSION_STATES.pop(user_id, None)

            await message.reply_text(
                "🎉 <b><u>Your String Session is Ready!</u></b>\n\n"
                f"<code>{session_str}</code>\n\n"
                "⚠️ <b>WARNING:</b> Never share this string session with anyone! Keep it safe.",
                quote=True,
            )
        except PasswordHashInvalid:
            await message.reply_text("❌ Incorrect 2FA password. Please try again:")
        except Exception as e:
            await message.reply_text(f"❌ Error verifying password: {e}\nSession generation aborted.")
            if client:
                try:
                    await client.disconnect()
                except Exception:
                    pass
            SESSION_STATES.pop(user_id, None)
