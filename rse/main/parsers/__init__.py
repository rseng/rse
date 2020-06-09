"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .github import GitHubParser
import re


def matches(Parser, uri):
    """Given a unique resource identifier, determine if it matches a regular expression
       used for a parser (or not)
    """
    if not hasattr(Parser, "matchstring"):
        raise NotImplementedError

    return not re.search(Parser.matchstring, uri) == None


def get_parser(uri, config=None):
    """get parser will return the correct parser depending on a uri
    """
    parser = None
    if matches(GitHubParser, uri):
        parser = GitHubParser(uri)

    if not parser:
        raise NotImplementedError("There is no matching parser for {uri}")
    parser.config = config
    return parser


def get_named_parser(name, uri=None, config=None):
    """get a named parser, meaning determining based on name and not uri
    """
    parser = None
    if re.search("github", name):
        parser = GitHubParser(uri)

    if not parser:
        raise NotImplementedError("There is no matching parser for {name}")

    parser.config = config
    return parser
