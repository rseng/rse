"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.scrapers import get_importer
import logging

bot = logging.getLogger("rse.client")


def main(args, extra):

    try:
        importer = get_importer(args.import_type)
    except:
        bot.exit(f"{args.import_type} is not a known importer.")

    results = importer.scrape(extra)
    print("Found %s results" % len(results))

    # If we have results and it's not a dry run, create the repos
    if results and not args.dry_run:
        importer.create(
            database=args.database, config_file=args.config_file, update=args.update
        )
