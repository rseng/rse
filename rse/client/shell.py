"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
from rse.defaults import RSE_SHELL


def main(args, extra):

    lookup = {"ipython": ipython, "python": python, "bpython": bpython}
    shells = ["ipython", "python", "bpython"]

    # Provide shell if available
    shell = RSE_SHELL.lower()
    if shell in lookup:
        try:
            return lookup[shell](args)
        except ImportError:
            pass

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](args)
        except ImportError:
            pass


def ipython(args):
    """give the user an ipython shell, optionally with an endpoint of choice."""
    client = Encyclopedia(config_file=args.config_file)
    assert client
    from IPython import embed

    embed()


def bpython(args):
    import bpython

    client = Encyclopedia(config_file=args.config_file)
    assert client
    bpython.embed(locals_={"client": client})


def python(args):
    import code

    client = Encyclopedia(config_file=args.config_file)
    assert client

    code.interact(local={"client": client})
