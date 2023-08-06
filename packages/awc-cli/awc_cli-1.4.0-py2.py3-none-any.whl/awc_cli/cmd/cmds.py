#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""user commands"""

import typing

from .admin_cmds import ADMIN_CMDS
from .mgr import CommandManager
from .user_cmds import USER_CMDS

CMGR: typing.Final[CommandManager] = CommandManager()

CMGR.register(USER_CMDS)
CMGR.register(ADMIN_CMDS)
