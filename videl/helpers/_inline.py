# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Modern Inline Keyboard Markup System with ButtonStyle

from typing import Dict, Any, Optional
from pyrogram import types
from videl.core.lang import lang_codes
from videl.helpers.button_style import ButtonStyle, styled_button


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                styled_button(text=f"❌ {text}", callback_data="cancel_dl", style=ButtonStyle.DANGER)
            ]
        ])

    def controls(
        self,
        chat_id: int,
        status: Optional[str] = None,
        timer: Optional[str] = None,
        remove: bool = False,
        is_playing: bool = True,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []

        # Row 1: Status / Progress Bar
        if status:
            keyboard.append([
                styled_button(text=f"📊 {status}", callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY)
            ])
        elif timer:
            keyboard.append([
                styled_button(text=f"⏱ {timer}", callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY)
            ])

        if not remove:
            # Row 2: Playback Controls
            play_pause_btn = (
                styled_button(text="⏸ Pause", callback_data=f"controls pause {chat_id}", style=ButtonStyle.PRIMARY)
                if is_playing
                else styled_button(text="▶️ Resume", callback_data=f"controls resume {chat_id}", style=ButtonStyle.SUCCESS)
            )
            keyboard.append([
                styled_button(text="⏮", callback_data=f"controls seekback {chat_id}"),
                play_pause_btn,
                styled_button(text="⏭", callback_data=f"controls skip {chat_id}"),
                styled_button(text="🔄", callback_data=f"controls replay {chat_id}"),
                styled_button(text="⏹", callback_data=f"controls stop {chat_id}", style=ButtonStyle.DANGER),
            ])

            # Row 3: Audio Tools & Effects
            keyboard.append([
                styled_button(text="🔁 Loop", callback_data=f"controls loop {chat_id}"),
                styled_button(text="🔀 Shuffle", callback_data=f"controls shuffle {chat_id}"),
                styled_button(text="🔊 Volume", callback_data=f"controls vol_menu {chat_id}"),
                styled_button(text="⚡ Speed", callback_data=f"controls speed_menu {chat_id}"),
                styled_button(text="📜 Lyrics", callback_data=f"controls lyrics {chat_id}"),
            ])

            # Row 4: Queue & Settings
            keyboard.append([
                styled_button(text="📋 Queue", callback_data=f"controls queue {chat_id}"),
                styled_button(text="⚙️ Settings", callback_data="settings"),
                styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER),
            ])

        return self.ikm(keyboard)

    def help_markup(self, _lang: Dict[str, Any], back: bool = False) -> types.InlineKeyboardMarkup:
        from videl import config
        if back:
            rows = [
                [
                    styled_button(text=f"🔙 {_lang['back']}", callback_data="help back", style=ButtonStyle.DEFAULT),
                    styled_button(text=f"❌ {_lang['close']}", callback_data="help close", style=ButtonStyle.DANGER),
                ]
            ]
        else:
            cbs = [
                ("admins", _lang.get("help_0", "Admins")),
                ("auth", _lang.get("help_1", "Auth")),
                ("blist", _lang.get("help_2", "Blacklist")),
                ("lang", _lang.get("help_3", "Language")),
                ("ping", _lang.get("help_4", "Ping")),
                ("play", _lang.get("help_5", "Play")),
                ("queue", _lang.get("help_6", "Queue")),
                ("stats", _lang.get("help_7", "Stats")),
                ("sudo", _lang.get("help_8", "Sudoers")),
            ]
            buttons = [
                styled_button(text=title, callback_data=f"help {cb}", style=ButtonStyle.DEFAULT)
                for cb, title in cbs
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            rows.append([
                styled_button(text="💬 Support Chat", url=config.SUPPORT_CHAT, style=ButtonStyle.PRIMARY),
                styled_button(text="❌ Close", callback_data="help close", style=ButtonStyle.DANGER),
            ])

        return self.ikm(rows)

    def lang_markup(self, _current_lang: str) -> types.InlineKeyboardMarkup:
        from videl import lang
        langs = lang.get_languages()
        buttons = [
            styled_button(
                text=f"{name} ({code}) {'✔️' if code == _current_lang else ''}",
                callback_data=f"lang_change {code}",
                style=ButtonStyle.SUCCESS if code == _current_lang else ButtonStyle.DEFAULT,
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        rows.append([
            styled_button(text="🔙 Back", callback_data="settings", style=ButtonStyle.DEFAULT)
        ])
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        from videl import config
        return self.ikm([
            [
                styled_button(text=f"💬 {text}", url=config.SUPPORT_CHAT, style=ButtonStyle.PRIMARY),
                styled_button(text="📢 Channel", url=config.SUPPORT_CHANNEL, style=ButtonStyle.DEFAULT),
            ]
        ])

    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                styled_button(
                    text=f"⚡️ {_text}",
                    callback_data=f"controls force {chat_id} {item_id}",
                    style=ButtonStyle.PRIMARY,
                )
            ]
        ])

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        _style = ButtonStyle.PRIMARY if playing else ButtonStyle.SUCCESS
        return self.ikm([
            [
                styled_button(text=f"⏯ {_text}", callback_data=f"controls {_action} {chat_id} q", style=_style),
                styled_button(text="🔀 Shuffle", callback_data=f"controls shuffle {chat_id}", style=ButtonStyle.DEFAULT),
            ],
            [
                styled_button(text="🗑 Close", callback_data="help close", style=ButtonStyle.DANGER)
            ]
        ])

    def settings_markup(
        self, _lang: Dict[str, Any], admin_only: bool, cmd_delete: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        admin_status = "🔒 Admins Only" if admin_only else "🌐 Everyone"
        cmd_status = "✅ Enabled" if cmd_delete else "❌ Disabled"
        lang_name = lang_codes.get(language, language)

        return self.ikm([
            [
                styled_button(text=f"{_lang.get('play_mode', 'Play Mode')}:", callback_data="settings"),
                styled_button(text=admin_status, callback_data="settings play", style=ButtonStyle.PRIMARY if admin_only else ButtonStyle.DEFAULT),
            ],
            [
                styled_button(text=f"{_lang.get('cmd_delete', 'Clean Mode')}:", callback_data="settings"),
                styled_button(text=cmd_status, callback_data="settings delete", style=ButtonStyle.SUCCESS if cmd_delete else ButtonStyle.DANGER),
            ],
            [
                styled_button(text=f"{_lang.get('language', 'Language')}:", callback_data="settings"),
                styled_button(text=f"🌐 {lang_name}", callback_data="language", style=ButtonStyle.PRIMARY),
            ],
            [
                styled_button(text="❌ Close", callback_data="help close", style=ButtonStyle.DANGER)
            ]
        ])

    def start_key(
        self, _lang: Dict[str, Any], private: bool = False
    ) -> types.InlineKeyboardMarkup:
        from videl import app, config
        bot_username = getattr(app, "username", "VidelMusicBot") or "VidelMusicBot"
        rows = [
            [
                styled_button(
                    text=f"➕ {_lang.get('add_me', 'Add Me To Your Group')}",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                    style=ButtonStyle.PRIMARY,
                )
            ],
            [
                styled_button(text=f"❓ {_lang.get('help', 'Help & Commands')}", callback_data="help", style=ButtonStyle.SUCCESS),
                styled_button(text=f"🌐 {_lang.get('language', 'Language')}", callback_data="language", style=ButtonStyle.DEFAULT),
            ],
            [
                styled_button(text=f"💬 {_lang.get('support', 'Support')}", url=config.SUPPORT_CHAT),
                styled_button(text=f"📢 {_lang.get('channel', 'Channel')}", url=config.SUPPORT_CHANNEL),
            ],
        ]
        if private:
            rows.append([
                styled_button(
                    text=f"✨ {_lang.get('source', 'Repository')}",
                    url=config.GITHUB_REPO,
                    style=ButtonStyle.DEFAULT,
                )
            ])
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                styled_button(text="❐ Copy Link", copy_text=link, style=ButtonStyle.PRIMARY),
                styled_button(text="🎥 YouTube", url=link, style=ButtonStyle.DEFAULT),
            ]
        ])

    def volume_markup(self, chat_id: int, current_vol: int = 100) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                styled_button(text="🔈 25%", callback_data=f"controls vol {chat_id} 25"),
                styled_button(text="🔉 50%", callback_data=f"controls vol {chat_id} 50"),
                styled_button(text="🔊 100%", callback_data=f"controls vol {chat_id} 100", style=ButtonStyle.PRIMARY),
                styled_button(text="📢 150%", callback_data=f"controls vol {chat_id} 150"),
            ],
            [
                styled_button(text="🔙 Back to Player", callback_data=f"controls back {chat_id}", style=ButtonStyle.DEFAULT)
            ]
        ])

    def speed_markup(self, chat_id: int, current_speed: float = 1.0) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                styled_button(text="0.75x", callback_data=f"controls spd {chat_id} 0.75"),
                styled_button(text="1.0x (Normal)", callback_data=f"controls spd {chat_id} 1.0", style=ButtonStyle.PRIMARY),
                styled_button(text="1.25x", callback_data=f"controls spd {chat_id} 1.25"),
                styled_button(text="1.5x", callback_data=f"controls spd {chat_id} 1.5"),
            ],
            [
                styled_button(text="🔙 Back to Player", callback_data=f"controls back {chat_id}", style=ButtonStyle.DEFAULT)
            ]
        ])


buttons = Inline()
