# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Localization Engine

import json
import os
from functools import wraps
from typing import Dict, Any
from pyrogram import types

lang_codes: Dict[str, str] = {
    "en": "English",
    "hi": "हिन्दी",
    "es": "Español",
    "fr": "Français",
    "ru": "Русский",
    "ar": "العربية",
    "de": "Deutsch",
    "ja": "日本語",
    "pt": "Português",
    "tr": "Türkçe",
    "pa": "ਪੰਜਾਬੀ",
    "my": "မြန်မာ",
    "zh": "中文",
}


class Language:
    def __init__(self, locales_dir: str = "videl/locales"):
        self.locales_dir = locales_dir
        self.languages: Dict[str, Dict[str, Any]] = {}
        self.load_languages()

    def load_languages(self) -> None:
        if not os.path.exists(self.locales_dir):
            return
        for file in os.listdir(self.locales_dir):
            if file.endswith(".json"):
                code = file.replace(".json", "")
                path = os.path.join(self.locales_dir, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.languages[code] = json.load(f)
                except Exception:
                    pass

    def get_languages(self) -> Dict[str, str]:
        return {code: lang_codes.get(code, code) for code in self.languages}

    def get_dict(self, lang_code: str) -> Dict[str, Any]:
        return self.languages.get(lang_code, self.languages.get("en", {}))

    async def get_lang(self, chat_id: int) -> Dict[str, Any]:
        from videl import db
        code = await db.get_lang(chat_id)
        return self.get_dict(code)

    def language(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(client, update: types.Message | types.CallbackQuery, *args, **kwargs):
                from videl import db
                chat_id = update.chat.id if isinstance(update, types.Message) else update.message.chat.id
                lang_code = await db.get_lang(chat_id)
                lang_dict = self.get_dict(lang_code)
                setattr(update, "lang", lang_dict)
                return await func(client, update, *args, **kwargs)
            return wrapper
        return decorator
