"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
import logging
from rse.utils.file import write_file
import os

bot = logging.getLogger("rse.client")


def main(args, extra):

    enc = Encyclopedia(config_file=args.config_file)

    # Case 1: empty list indicates listing all
    if os.path.exists(args.path) and not args.force:
        bot.error("{args.path} already exists, use --force to overwrite it.")

    # We just want the unique id, the first result
    repos = [x[0] for x in enc.list()]
    write_file(args.path, "\n".join(repos))
    bot.info(f"Wrote {len(repos)} to {args.path}")
