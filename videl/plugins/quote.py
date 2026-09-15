# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Glassmorphic Message Quote Card Generator Plugin

import os
import textwrap
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import filters, types
from videl import app

FONT_PATH = "videl/helpers/Raleway-Bold.ttf"
BODY_FONT_PATH = "videl/helpers/Inter-Light.ttf"


def generate_quote_image(
    text: str,
    name: str,
    username: str,
    avatar_path: str = None,
    time_str: str = None,
) -> str:
    width = 800
    padding = 40

    # Fonts
    try:
        font_name = ImageFont.truetype(FONT_PATH, 26)
        font_user = ImageFont.truetype(BODY_FONT_PATH, 18)
        font_text = ImageFont.truetype(BODY_FONT_PATH, 24)
        font_time = ImageFont.truetype(BODY_FONT_PATH, 16)
    except Exception:
        font_name = font_user = font_text = font_time = ImageFont.load_default()

    # Wrap text
    lines = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(paragraph, width=38)
        lines.extend(wrapped if wrapped else [""])

    line_height = 34
    text_block_height = max(len(lines) * line_height, 60)
    height = max(180, 120 + text_block_height + padding * 2)

    # Base image with dark gradient
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Card background (Dark glassmorphic rounded rect)
    card_bounds = [(15, 15), (width - 15, height - 15)]
    draw.rounded_rectangle(card_bounds, radius=24, fill=(24, 28, 42, 240), outline=(56, 189, 248, 120), width=2)

    # Avatar
    avatar_size = 70
    avatar_x = 45
    avatar_y = 40

    if avatar_path and os.path.exists(avatar_path):
        try:
            av_img = Image.open(avatar_path).convert("RGBA")
            av_img = av_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
            # Circular mask
            mask = Image.new("L", (avatar_size, avatar_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
            av_circular = ImageOps.fit(av_img, mask.size, centering=(0.5, 0.5))
            av_circular.putalpha(mask)
            img.paste(av_circular, (avatar_x, avatar_y), av_circular)
        except Exception:
            draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size], fill=(59, 130, 246, 255))
    else:
        draw.ellipse([avatar_x, avatar_y, avatar_x + avatar_size, avatar_y + avatar_size], fill=(59, 130, 246, 255))
        init_letter = name[0].upper() if name else "U"
        draw.text((avatar_x + 24, avatar_y + 15), init_letter, fill=(255, 255, 255), font=font_name)

    # Name and username
    text_x = avatar_x + avatar_size + 24
    draw.text((text_x, avatar_y + 4), name[:30], fill=(255, 255, 255), font=font_name)
    draw.text((text_x, avatar_y + 36), f"@{username}" if username else "", fill=(148, 163, 184), font=font_user)

    # Timestamp
    if not time_str:
        time_str = datetime.now().strftime("%I:%M %p")
    draw.text((width - 140, avatar_y + 8), time_str, fill=(100, 116, 139), font=font_time)

    # Quote text
    curr_y = avatar_y + avatar_size + 25
    for line in lines:
        draw.text((avatar_x + 10, curr_y), line, fill=(241, 245, 249), font=font_text)
        curr_y += line_height

    out_path = f"cache/quote_{int(datetime.now().timestamp())}.png"
    os.makedirs("cache", exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path


@app.on_message(filters.command(["q", "quote"]) & ~app.bl_users)
async def quote_command(_, message: types.Message):
    target_msg = message.reply_to_message
    if not target_msg:
        return await message.reply_text("❌ Please reply to a message to generate a quote card.", quote=True)

    text = target_msg.text or target_msg.caption or "<i>[Media]</i>"
    user = target_msg.from_user or target_msg.sender_chat

    if not user:
        name = "Anonymous"
        username = ""
    elif isinstance(user, types.User):
        name = f"{user.first_name} {user.last_name or ''}".strip()
        username = user.username or ""
    else:
        name = user.title
        username = user.username or ""

    msg = await message.reply_text("🎨 Rendering glassmorphic quote card...", quote=True)

    avatar_path = None
    if isinstance(user, types.User) and user.photo:
        try:
            avatar_path = await app.download_media(user.photo.big_file_id)
        except Exception:
            pass

    time_str = target_msg.date.strftime("%I:%M %p") if target_msg.date else None
    card_path = generate_quote_image(
        text=text,
        name=name,
        username=username,
        avatar_path=avatar_path,
        time_str=time_str,
    )

    if avatar_path and os.path.exists(avatar_path):
        os.remove(avatar_path)

    await message.reply_photo(
        photo=card_path,
        caption=f"💬 <b>Quote by {name}</b>",
        quote=True,
    )
    if os.path.exists(card_path):
        os.remove(card_path)
    await msg.delete()
