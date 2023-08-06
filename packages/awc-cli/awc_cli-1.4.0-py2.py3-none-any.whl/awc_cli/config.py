#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""config"""

import os
import typing

INSTANCE: typing.Final[str] = os.environ.get("INSTANCE", "https://server.ari-web.xyz/")
KEY: typing.Final[typing.Optional[str]] = os.environ.get("KEY")
ADMIN_CLR: typing.Final[typing.Optional[str]] = os.environ.get("ADMIN_CLR", "\033[31m")

__all__: typing.Final[typing.Tuple[str, ...]] = (
    "INSTANCE",
    "KEY",
    "ADMIN_CLR",
)
