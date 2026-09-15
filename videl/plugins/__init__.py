# Copyright (c) 2026 Beasgohan-code
# Licensed under the MIT License.
# Videl Plugins Initializer

import os
import glob

def __list_all_modules():
    mod_paths = glob.glob(os.path.dirname(__file__) + "/*.py")
    all_modules = [
        os.path.basename(f)[:-3]
        for f in mod_paths
        if os.path.isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return sorted(all_modules)

all_modules = __list_all_modules()
__all__ = all_modules + ["all_modules"]
