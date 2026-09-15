# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Dynamic Aesthetic Thumbnail Generator

import os
import aiohttp
from typing import Optional, Tuple
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)
from videl import config, logger
from videl.helpers._dataclass import Track


class Thumbnail:
    def __init__(self):
        self.rect = (920, 520)
        self.fill = (255, 255, 255)
        self.accent_color = (255, 75, 140)  # Videl Pink/Magenta Accent
        self.mask = Image.new("L", self.rect, 0)
        
        font_path1 = "videl/helpers/Raleway-Bold.ttf"
        font_path2 = "videl/helpers/Inter-Light.ttf"

        try:
            self.font_title = ImageFont.truetype(font_path1, 32)
            self.font_meta = ImageFont.truetype(font_path2, 26)
            self.font_time = ImageFont.truetype(font_path1, 24)
            self.font_badge = ImageFont.truetype(font_path1, 20)
        except Exception:
            self.font_title = ImageFont.load_default()
            self.font_meta = ImageFont.load_default()
            self.font_time = ImageFont.load_default()
            self.font_badge = ImageFont.load_default()

        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    async def save_thumb(self, output_path: str, url: str) -> str:
        await self.start()
        async with self.session.get(url) as resp:
            content = await resp.read()
            with open(output_path, "wb") as f:
                f.write(content)
        return output_path

    async def generate(self, song: Track, size: Tuple[int, int] = (1280, 720)) -> str:
        try:
            temp = f"cache/temp_{song.id}.jpg"
            output = f"cache/{song.id}.png"
            if os.path.exists(output):
                return output

            thumb_url = song.thumbnail or config.DEFAULT_THUMB
            await self.save_thumb(temp, thumb_url)

            # Load and create blurred background
            thumb_img = Image.open(temp).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            blur = thumb_img.filter(ImageFilter.GaussianBlur(30))
            background = ImageEnhance.Brightness(blur).enhance(0.35)

            # Create rounded center card
            center_card = ImageOps.fit(thumb_img, self.rect, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            mask = Image.new("L", self.rect, 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, self.rect[0], self.rect[1]), radius=24, fill=255)
            center_card.putalpha(mask)

            # Paste card
            background.paste(center_card, (180, 40), center_card)

            # Draw UI Elements
            draw = ImageDraw.Draw(background)

            # Glowing Accent Border on Card
            draw.rounded_rectangle((178, 38, 180 + self.rect[0] + 2, 40 + self.rect[1] + 2), radius=26, outline=self.accent_color, width=3)

            # Artist / Channel Meta
            channel_info = f"⚡ {song.channel_name[:30]}" if song.channel_name else "⚡ Videl Music"
            if song.view_count:
                channel_info += f"  •  {song.view_count}"
            draw.text((60, 580), channel_info, font=self.font_meta, fill=(220, 220, 240))

            # Song Title
            title = song.title[:45] + ("..." if len(song.title) > 45 else "")
            draw.text((60, 615), title, font=self.font_title, fill=self.fill)

            # Timeline Progress Bar
            draw.text((60, 665), "00:01", font=self.font_time, fill=(200, 200, 200))
            # Bar background
            draw.rounded_rectangle([(145, 678), (1125, 686)], radius=4, fill=(80, 80, 95))
            # Bar active progress
            draw.rounded_rectangle([(145, 678), (420, 686)], radius=4, fill=self.accent_color)
            # Active indicator circle
            draw.ellipse([(414, 674), (428, 690)], fill=(255, 255, 255))
            draw.text((1140, 665), song.duration or "Live", font=self.font_time, fill=(200, 200, 200))

            background.save(output, format="PNG")
            try:
                if os.path.exists(temp):
                    os.remove(temp)
            except Exception:
                pass
            return output
        except Exception as ex:
            logger.warning(f"Failed to generate thumbnail for {song.id}: {ex}")
            return config.DEFAULT_THUMB
