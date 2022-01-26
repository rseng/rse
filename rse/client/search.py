"""

Copyright (C) 2020-2022 Vanessa Sochat.

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

    # We can search taxonomy, criteria, or both
    taxonomy = args.taxonomy or []
    criteria = args.criteria or []
    if not query and not taxonomy and not criteria:
        sys.exit("Please provide a query to search for.")
    results = enc.search(query, taxonomy=taxonomy, criteria=criteria)
    if results:
        for key, listing in results.items():
            bot.info(key)
            bot.table(listing)
            bot.newline()
