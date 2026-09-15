# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl RichMessage & Structured Blocks System

from typing import List, Optional, Dict, Any
from enum import Enum


class BlockType(str, Enum):
    HEADER = "header"
    TEXT = "text"
    BLOCKQUOTE = "blockquote"
    PULL_QUOTE = "pull_quote"
    LIST = "list"
    DIVIDER = "divider"
    CODE = "code"


class RichBlock:
    """Represents a structured block inside a rich formatted message."""
    def __init__(
        self,
        block_type: BlockType,
        content: str,
        author: Optional[str] = None,
        expandable: bool = False,
        language: Optional[str] = None,
    ):
        self.block_type = block_type
        self.content = content
        self.author = author
        self.expandable = expandable
        self.language = language

    def to_html(self) -> str:
        if self.block_type == BlockType.HEADER:
            return f"<b><u>{self.content}</u></b>\n"
        elif self.block_type == BlockType.BLOCKQUOTE:
            attr = " expandable" if self.expandable else ""
            return f"<blockquote{attr}>{self.content}</blockquote>"
        elif self.block_type == BlockType.PULL_QUOTE:
            author_str = f"\n<i>— {self.author}</i>" if self.author else ""
            return f"<blockquote expandable><b>“{self.content}”</b>{author_str}</blockquote>"
        elif self.block_type == BlockType.CODE:
            lang_attr = f' class="language-{self.language}"' if self.language else ""
            return f"<pre{lang_attr}><code>{self.content}</code></pre>"
        elif self.block_type == BlockType.DIVIDER:
            return "──────────────────────────"
        elif self.block_type == BlockType.LIST:
            return self.content
        return self.content

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.block_type.value,
            "content": self.content,
            "author": self.author,
            "expandable": self.expandable,
            "language": self.language,
        }


class RichMessage:
    """
    Builder for structured Bot API 10.x+ Rich Messages and formatted HTML/Markdown cards.
    """
    def __init__(self, title: Optional[str] = None):
        self.title = title
        self.blocks: List[RichBlock] = []

    def add_header(self, text: str) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.HEADER, text))
        return self

    def add_text(self, text: str) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.TEXT, text))
        return self

    def add_blockquote(self, text: str, expandable: bool = False) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.BLOCKQUOTE, text, expandable=expandable))
        return self

    def add_pull_quote(self, text: str, author: Optional[str] = None) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.PULL_QUOTE, text, author=author, expandable=True))
        return self

    def add_code(self, code: str, language: Optional[str] = None) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.CODE, code, language=language))
        return self

    def add_divider(self) -> "RichMessage":
        self.blocks.append(RichBlock(BlockType.DIVIDER, ""))
        return self

    def render_html(self) -> str:
        """Render entire rich message to Telegram HTML format."""
        parts = []
        if self.title:
            parts.append(f"<b><u>{self.title}</u></b>\n")
        for block in self.blocks:
            parts.append(block.to_html())
        return "\n\n".join(parts)

    def render_markdown(self) -> str:
        """Render to Telegram Rich Markdown."""
        parts = []
        if self.title:
            parts.append(f"**{self.title}**\n")
        for block in self.blocks:
            if block.block_type == BlockType.HEADER:
                parts.append(f"## {block.content}")
            elif block.block_type == BlockType.BLOCKQUOTE:
                parts.append(f"> {block.content}")
            elif block.block_type == BlockType.CODE:
                lang = block.language or ""
                parts.append(f"```{lang}\n{block.content}\n```")
            elif block.block_type == BlockType.DIVIDER:
                parts.append("---")
            else:
                parts.append(block.content)
        return "\n\n".join(parts)

    @staticmethod
    def badge(text: str, emoji: str = "⚡️") -> str:
        return f"<code>{emoji} {text}</code>"

    @staticmethod
    def progress_bar(current: int, total: int, length: int = 12) -> str:
        if total <= 0:
            return "🔘" + "═" * (length - 1)
        ratio = min(max(current / total, 0.0), 1.0)
        pos = min(int(ratio * length), length - 1)
        return "═" * pos + "🔘" + "═" * (length - pos - 1)
