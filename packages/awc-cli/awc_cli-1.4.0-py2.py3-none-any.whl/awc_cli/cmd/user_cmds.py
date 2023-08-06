#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""user commands"""

import typing

import awc
import awc.api
import awc.exc
import lxml.etree as etree  # type: ignore

from ..config import ADMIN_CLR
from ..util import err
from . import Command
from .mgr import CommandManager

USER_CMDS: typing.Final[CommandManager] = CommandManager()


@USER_CMDS.new
@USER_CMDS.nonempty
def post(api: awc.Awc, cmd: Command) -> int:
    """post a new comment
    usage : post <comment content>"""

    comment: typing.List[typing.Union[int, bool]] = awc.api.post_comment(api, cmd.cmd)

    print(
        f"posted comment #{comment[0]} as",
        "admin" if comment[1] else "user",
    )

    return 0


@USER_CMDS.new
@USER_CMDS.nonempty
def get(api: awc.Awc, cmd: Command) -> int:
    """get a range of comments
    usage : get <from> <to>
    where : diff(from, to) <= 25"""

    from_cid: int
    to_cid: int

    try:
        from_cid, to_cid = tuple(map(lambda s: int(s or ""), (cmd.next(), cmd.next())))
    except ValueError:
        return err("not enough arguments / invalid argument types")

    try:
        comments: typing.Dict[
            str, typing.List[typing.Union[str, bool, None]]
        ] = awc.api.get_comments(api, from_cid, to_cid)
    except ValueError:
        return err("invalid both or one of `from`, `to`")

    for cid, meta in comments.items():
        print(f"#{cid} {ADMIN_CLR if meta[2] else ''}{meta[0]!r}\033[0m : {meta[1]}")

    return 0


@USER_CMDS.new
@USER_CMDS.nonempty
def get1(api: awc.Awc, cmd: Command) -> int:
    """get a single comment
    usage : get1 <id>
    which : get <id> <id>"""

    cmd.cmd += f" {cmd.cmd}"

    return get(api, cmd)


@USER_CMDS.new
def total(api: awc.Awc, *_: typing.Any) -> int:
    """get total comments count
    usage : total"""

    print(awc.api.total(api))
    return 0


@USER_CMDS.new
def islocked(api: awc.Awc, *_: typing.Any) -> int:
    """are the comments locked
    usage : islocked"""

    print(awc.api.get_comment_lock(api))
    return 0


@USER_CMDS.new
def amiadmin(api: awc.Awc, *_: typing.Any) -> int:
    """do you have admin rights
    usage : amiadmin"""

    print(awc.api.amiadmin(api))
    return 0


@USER_CMDS.new
def apikey(api: awc.Awc, cmd: Command) -> int:
    """set the api key ( or unset it )
    usage : apikey [api key]"""

    api.api_key = cmd.cmd or None
    return 0


@USER_CMDS.new
@USER_CMDS.nonempty
def anon(api: awc.Awc, cmd: Command) -> int:
    """post an anonymous message
    usage : anon <message>"""

    print(awc.api.anon(api, cmd.cmd))
    return 0


@USER_CMDS.new
def visits(api: awc.Awc, *_: typing.Any) -> int:
    """get visit count
    usage : visits"""

    print(
        etree.fromstring(awc.api.visit(api))  # type: ignore
        .xpath("//svg:text", namespaces={"svg": "http://www.w3.org/2000/svg"})[0]
        .text
    )

    return 0
