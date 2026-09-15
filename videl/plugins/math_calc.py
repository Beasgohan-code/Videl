# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Math Evaluator & LaTeX Formula Formatter Plugin

import math
from pyrogram import filters, types
from videl import app
from videl.helpers.rich_ui import render_table


# Safe math scope
SAFE_MATH = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "sqrt": math.sqrt,
    "cbrt": math.cbrt if hasattr(math, "cbrt") else lambda x: x ** (1 / 3),
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "pow": math.pow,
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "factorial": math.factorial,
    "degrees": math.degrees,
    "radians": math.radians,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
}


def pretty_format_math(expr: str) -> str:
    """Replaces standard operators with clean Unicode math symbols."""
    formatted = expr
    formatted = formatted.replace("*", " × ")
    formatted = formatted.replace("/", " ÷ ")
    formatted = formatted.replace("**", " ^ ")
    formatted = formatted.replace("sqrt", "√")
    formatted = formatted.replace("pi", "π")
    return formatted


@app.on_message(filters.command(["math", "calc", "calculate", "formula"]) & ~app.bl_users)
async def math_command(_, message: types.Message):
    if len(message.command) < 2:
        table_example = render_table(
            ["Function", "Syntax", "Output"],
            [
                ["Square Root", "sqrt(144)", "12.0"],
                ["Trigonometry", "sin(pi / 2)", "1.0"],
                ["Power", "pow(2, 10)", "1024.0"],
                ["Factorial", "factorial(6)", "720"],
            ],
            style="box",
        )
        return await message.reply_text(
            f"📐 <b><u>Videl Rich Math & Formula Evaluator</u></b>\n\n"
            f"<b>Usage:</b> <code>/math [mathematical expression]</code>\n\n"
            f"<b>Supported Functions:</b>\n{table_example}\n"
            f"<i>Example:</i> <code>/math sqrt(256) * cos(0) + 2^8</code>",
            quote=True,
        )

    raw_expr = message.text.split(None, 1)[1].strip()
    clean_expr = raw_expr.replace("^", "**").replace("×", "*").replace("÷", "/")

    try:
        # Safe eval using math dictionary
        result = eval(clean_expr, {"__builtins__": None}, SAFE_MATH)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        pretty_input = pretty_format_math(raw_expr)

        table_res = render_table(
            ["Field", "Value"],
            [
                ["Input Expression", raw_expr],
                ["Standard Form", pretty_input],
                ["Calculated Result", str(result)],
            ],
            style="box",
        )

        output = (
            f"🧮 <b><u>Mathematical Computation</u></b>\n\n"
            f"{table_res}\n"
            f"<blockquote expandable>\n"
            f"<b>Formula:</b> <code>{raw_expr} = {result}</code>\n"
            f"<b>Precision:</b> Standard IEEE-754 64-bit Floating Point\n"
            f"</blockquote>"
        )
        await message.reply_text(output, quote=True)

    except Exception as e:
        await message.reply_text(f"❌ <b>Math Error:</b> <code>{e}</code>\nCheck your formula syntax.", quote=True)
