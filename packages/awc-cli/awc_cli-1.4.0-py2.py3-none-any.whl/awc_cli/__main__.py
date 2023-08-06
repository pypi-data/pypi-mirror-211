#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""awc cli -- main"""

from warnings import filterwarnings as filter_warnings

import awc
import awc.api

from .config import INSTANCE, KEY
from .repl import repl


def main() -> int:
    """entry / main function"""

    with awc.Awc(INSTANCE, KEY) as awc_api:
        awc.api.visit(awc_api)
        return repl(awc_api)


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"

    filter_warnings("error", category=Warning)
    raise SystemExit(main())
