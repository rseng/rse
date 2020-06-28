"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.scrapers import get_named_scraper
import sys


def main(args, extra):

    try:
        scraper = get_named_scraper(args.scraper_name[0])
    except:
        sys.exit(f"{args.scraper_name[0]} is not a known scraper.")

    # Either get latest entries, or based on search
    if args.query is not None:
        results = scraper.search(args.query, delay=args.delay)
    else:
        results = scraper.latest(delay=args.delay)
    print("Found %s results" % len(results))

    # If we have results and it's not a dry run, create the repos
    if results and not args.dry_run:
        scraper.create(database=args.database, config_file=args.config_file)
