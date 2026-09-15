# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Directory Initializer

import os
import shutil


def ensure_dirs() -> None:
    """Ensure all required runtime directories exist and are clean."""
    directories = ["cache", "downloads", "cookies", "videl/locales"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def clean_temp_dirs() -> None:
    """Clean transient download & cache files upon restart."""
    for directory in ["cache", "downloads"]:
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
            os.makedirs(directory, exist_ok=True)
