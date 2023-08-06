#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""command parser"""

import typing


class Command:
    """command parser"""

    __slots__: typing.Tuple[str] = ("cmd",)

    def __init__(self, cmd: str) -> None:
        self.cmd: str = cmd.strip()

    def next(
        self,
    ) -> typing.Optional[str]:
        """get next command token"""

        if not self.cmd:
            return None

        head, self.cmd = (self.cmd.strip().split(maxsplit=1) + [""])[:2]
        return head
