#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli utils"""

import sys
import typing

import awc
import awc.api
import awc.exc
import awc.sql
import awc.sql.helpers
import pypika.queries  # type: ignore


def awc_input(prompt: str) -> str:
    """custom input prompt + infinite ask"""

    val: str = ""

    while not val:
        try:
            val = input(f"{prompt} :: ").strip()
        except KeyboardInterrupt:
            print()
            continue
        except EOFError as eof:
            print()
            raise eof

    return val


def err(msg: str) -> int:
    """print an error message and return error code"""

    print(f"err : {msg}", file=sys.stderr)
    return 1


def accept_application(
    api: awc.Awc, user: typing.Optional[str] = None
) -> typing.Optional[str]:
    """accept a users application, return value is the username if succeeded"""

    if api.api_key is None:
        return None

    if user is not None:
        awc.api.sql(api, awc.sql.multisql(awc.sql.helpers.whitelist(user)))
        return user

    while True:
        try:
            awc.api.sql(
                api,
                awc.sql.multisql(
                    awc.sql.helpers.whitelist(
                        (user := awc_input("what username did you apply with"))
                    )
                ),
            )
            break
        except awc.exc.APIRequestFailedError as e:
            err(
                f"failed to whitelist you : HTTP/{e.response.status_code} -- \
{e.response.text[-20:]!r}"
            )
            continue

    return user


def run_sql(
    api: awc.Awc, sql: typing.List[pypika.queries.QueryBuilder]
) -> typing.List[typing.List[typing.Any]]:
    """run sql on the API"""

    return awc.api.sql(api, awc.sql.multisql(sql))
