"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
from rse.logger import bot


def main(args, extra):

    # Create a queue object, run the command to match to an executor
    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    # Case 1: empty list indicates listing all
    if not args.parser:
        bot.table(enc.list())
    else:
        # Each in the list can be a full executor or a uid
        for parser in args.parser:
            bot.table(enc.list(parser))
