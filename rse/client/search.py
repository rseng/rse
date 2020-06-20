"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
from rse.logger import bot
import sys


def main(args, extra):

    enc = Encyclopedia(config_file=args.config_file, database=args.database)
    query = " ".join(args.query).strip()
    if not query:
        sys.exit("Please provide a query to search for.")
    results = enc.search(query)
    if results:
        bot.table(results)
