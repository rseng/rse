"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
import logging

bot = logging.getLogger("rse.client")


def main(args, extra):

    enc = Encyclopedia(config_file=args.config_file)

    # Case 1: empty list indicates listing all
    if not args.uid:
        bot.error("Please provide a unique resource identifier to search for.")
    else:
        if enc.exists(args.uid):
            print(f"{args.uid} exists.")
        else:
            print(f"{args.uid} does not exist.")
