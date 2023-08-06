#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repl"""

import typing

import awc
import awc.api
import awc.exc

from .cmd import Command
from .cmd.cmds import CMGR
from .util import accept_application, awc_input, err


def run_cmd_fn(
    fn: typing.Callable[[awc.Awc, Command], int],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> int:
    """run command handing commong exceptions"""

    msg: typing.Optional[str] = None

    try:
        return fn(*args, **kwargs)
    except awc.exc.APIRequestFailedError as e:
        msg = f"API request to {e.api!r} api failed, \
got {e.response.status_code} : {e.response.text!r}"
    except awc.exc.InvalidAPIKeyError:
        msg = "invalid API key"
    except awc.exc.UnexpectedResponseError as e:
        msg = f"unexpected API response non-{e.expected} : {e.value!r}"
    except awc.exc.ResouceNotFoundError as e:
        msg = f"resource not found : {e.value!r}"
    except Exception as e:
        msg = f"{e.__class__.__name__} -- {e}"
    finally:
        return 0 if msg is None else err(msg)


def repl_shell(user: str, api: awc.Awc) -> int:
    """main repl shell"""

    try:
        import readline

        del readline
    except Exception:
        pass

    last: int = 0

    print(
        "type `help` for help, press CTRL + D or type `.exit` to exit,"
        " you can use escapes like \\n in command input"
    )

    while True:
        try:
            print()
            cmd: Command = Command(
                awc_input(f"[{last}] {user}@{api.instance.host}")  # type: ignore
                .encode()
                .decode("unicode_escape")
            )
        except UnicodeError as ue:
            last = err(str(ue))
            continue
        except EOFError:
            break

        if cmd.cmd == ".exit":
            break

        if (cfn := CMGR.get((cname := cmd.next()))) is None:
            last = err(f"{cname!r} -- command not found")
            continue

        last = run_cmd_fn(cfn, api, cmd)

    return last


def repl(api: awc.Awc) -> int:
    """the repl main"""

    user: typing.Optional[str]

    try:
        user = awc.api.whoami(api)
    except awc.exc.APIRequestFailedError:
        if awc_input("do you want to apply [Y/n]").lower().startswith("n"):
            print("not applying, some functions might not work")
            return repl_shell("#", api)

        if awc.api.applied(api):
            if (user := accept_application(api)) is None:
                return err("please wait for your application to get accepted")
        else:
            print("please apply")

            try:
                awc.api.apply(
                    api,
                    (user := awc_input("username")),
                    awc_input("why do you want to apply"),
                )
            except EOFError:
                return 2

            if accept_application(api, user) is None:
                return err("cannot accept your application, wait for your acceptance")

    return repl_shell(user, api)
