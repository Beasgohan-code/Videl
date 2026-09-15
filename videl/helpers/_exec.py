# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Eval Execution Engine

import ast
import traceback
from typing import Any, Dict


def format_exception(exc: Exception, tb: list) -> str:
    return "".join(traceback.format_exception_only(type(exc), exc)) + "".join(traceback.format_list(tb))


async def meval(code: str, globs: Dict[str, Any], **kwargs: Any) -> Any:
    locs = {}
    globs.update(kwargs)

    # Clean code formatting
    lines = code.strip().split("\n")
    if len(lines) == 1:
        try:
            tree = ast.parse(f"_eval_res = {code}")
            compiled = compile(tree, "<string>", "exec")
            exec(compiled, globs, locs)
            return locs.get("_eval_res")
        except SyntaxError:
            pass

    # Async function wrapper for multi-line evaluation
    indented = "\n".join(f"    {line}" for line in lines)
    func_code = f"async def _eval_func():\n{indented}"
    exec(func_code, globs, locs)
    func = locs["_eval_func"]
    return await func()
