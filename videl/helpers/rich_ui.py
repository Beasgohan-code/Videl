# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Rich UI, Unicode Tables, Math & Media Card Rendering Engine

from typing import List, Optional, Dict, Any


def render_heading(title: str, subtitle: Optional[str] = None, icon: str = "⚡") -> str:
    """Renders a stylized Telegram heading banner."""
    top = f"╔════════════════════════════════════╗\n"
    mid = f"║  {icon} <b>{title.upper()}</b>\n"
    if subtitle:
        mid += f"║  <i>{subtitle}</i>\n"
    bot = f"╚════════════════════════════════════╝"
    return f"{top}{mid}{bot}"


def render_table(headers: List[str], rows: List[List[Any]], style: str = "box") -> str:
    """
    Renders a formatted Unicode box-drawing table.
    Styles: 'box' (┌─┬─┐), 'simple' (| - |), 'dots' (╒═╤═╕)
    """
    if not headers or not rows:
        return ""

    # Convert all cells to strings
    s_headers = [str(h) for h in headers]
    s_rows = [[str(cell) for cell in row] for row in rows]

    num_cols = len(s_headers)
    col_widths = [len(h) for h in s_headers]

    for row in s_rows:
        for i in range(min(len(row), num_cols)):
            col_widths[i] = max(col_widths[i], len(row[i]))

    # Padding helper
    def pad(val: str, width: int) -> str:
        return val + " " * (width - len(val))

    if style == "box":
        top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐\n"
        head_str = "│ " + " │ ".join(pad(h, col_widths[i]) for i, h in enumerate(s_headers)) + " │\n"
        sep = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤\n"
        row_strs = [
            "│ " + " │ ".join(pad(r[i] if i < len(r) else "", col_widths[i]) for i in range(num_cols)) + " │\n"
            for r in s_rows
        ]
        bot = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
        return f"<pre>\n{top}{head_str}{sep}{''.join(row_strs)}{bot}\n</pre>"

    else:
        # Simple markdown table
        head_str = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(s_headers)) + " |\n"
        sep = "| " + " | ".join("-" * col_widths[i] for i in range(num_cols)) + " |\n"
        row_strs = [
            "| " + " | ".join(pad(r[i] if i < len(r) else "", col_widths[i]) for i in range(num_cols)) + " |\n"
            for r in s_rows
        ]
        return f"<pre>\n{head_str}{sep}{''.join(row_strs)}\n</pre>"


def render_spectrum_bar(progress_ratio: float = 0.5) -> str:
    """Generates an animated audio frequency spectrum visualizer."""
    bars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    patterns = [
        " ▃▅▆▇▆▅▃ ",
        "▃▅▇█▇▅▃ ",
        "▅▇▆▅▃ ▃▅",
        "▇▅▃ ▃▅▆▇",
    ]
    idx = int(progress_ratio * len(patterns)) % len(patterns)
    return patterns[idx]


def render_quote_card(text: str, author: str, title: Optional[str] = None) -> str:
    """Renders a styled expandable quote block."""
    card = ""
    if title:
        card += f"💬 <b>{title}</b>\n\n"
    card += f"<blockquote expandable>\n<i>“{text}”</i>\n\n— <b>{author}</b>\n</blockquote>"
    return card


def render_media_card(
    heading: str,
    caption: str,
    metadata: Dict[str, Any],
    quote_text: Optional[str] = None,
) -> str:
    """Renders a rich structured media card caption."""
    header_block = f"🌟 <b><u>{heading}</u></b>\n\n"
    desc_block = f"{caption}\n\n"

    # Metadata table / bullet list
    meta_lines = []
    for k, v in metadata.items():
        meta_lines.append(f"• <b>{k}:</b> <code>{v}</code>")
    meta_block = "\n".join(meta_lines) + "\n"

    quote_block = ""
    if quote_text:
        quote_block = f"\n<blockquote expandable>“{quote_text}”</blockquote>\n"

    return f"{header_block}{desc_block}{meta_block}{quote_block}"
