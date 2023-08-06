#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""command managerhttps://github.com/felixonmars"""

import typing
from copy import deepcopy
from functools import wraps

from awc import Awc

from .. import __version__ as awc_cli_version
from ..config import __all__ as conf_vars
from ..util import err
from . import Command


class CommandManager:
    """command manager"""

    __slots__: typing.Tuple[str, ...] = (
        "__cmds",
        "__admin",
    )

    @property
    def cmds(self) -> typing.Dict[str, typing.Callable[[Awc, Command], int]]:
        """return a copy of all commands"""
        return deepcopy(self.__cmds)

    @property
    def admin(self) -> bool:
        """is this manager context admin-only"""
        return self.__admin

    def __help(self, *_: typing.Any) -> int:
        """help
        usage : help"""

        print(
            f"""commands for awc-cli version {awc_cli_version}
*command = requires an API key
"""
        )

        for cmd, cfn in self.__cmds.items():
            header: str = (
                f"{(('*' if getattr(cfn, '__auth__', False) else '') + cmd):<15}"
            )

            print(header, end="")

            for idx, docline in enumerate(
                (cfn.__doc__ or "no help provided").splitlines()
            ):
                docline = docline.strip()
                print(f"-- {docline}" if idx == 0 else f"{' ' * len(header)}{docline}")

        print("\ncustomisable environment variables :\n")

        for env in conf_vars:
            print(f"${env}")

        return 0

    def __init__(self, admin: bool = False) -> None:
        self.__cmds: typing.Dict[str, typing.Callable[[Awc, Command], int]] = {
            "help": self.__help
        }
        self.__admin = admin

    def new(
        self,
        f: typing.Callable[[Awc, Command], int],
    ) -> typing.Callable[[Awc, Command], int]:
        """register a new command"""

        if not self.admin:
            self.__cmds[f.__name__] = f
            return f

        setattr(f, "__auth__", True)

        @wraps(f)
        def wrap(api: Awc, cmd: Command) -> int:
            return (
                err(f"{f.__name__!r} requires an API key to be set")
                if api.api_key is None
                else f(api, cmd)
            )

        self.__cmds[f.__name__] = wrap
        return wrap

    def nonempty(
        self,
        f: typing.Callable[[Awc, Command], int],
    ) -> typing.Callable[[Awc, Command], int]:
        """dont allow for no arguments in a command"""

        @wraps(f)
        def wrap(api: Awc, cmd: Command) -> int:
            return (
                f(api, cmd)
                if cmd.cmd
                else err(f"{f.__name__!r} requires argument( s )")
            )

        return wrap

    def get(
        self, name: typing.Optional[str]
    ) -> typing.Optional[typing.Callable[[Awc, Command], int]]:
        """get command by name"""
        return None if name is None else self.__cmds.get(name)

    def clear(self) -> None:
        """set commands to nothing"""

        self.__cmds.clear()

    def register(self, manager: "CommandManager") -> None:
        """register commands from an external manager"""

        self.__cmds.update(manager.cmds)
        self.__cmds["help"] = self.__help

        manager.clear()
