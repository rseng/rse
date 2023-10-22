"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import sys

from rse.main.scrapers import get_importer


def parse_extra(extra):
    """
    Allow for basic parsing of extra args, in form <arg>=<value> only.
    """
    args = []
    kwargs = {}
    for arg in extra:
        # This is a key value pair (extra)
        if arg.startswith("--") and "=" in arg:
            key, val = arg.strip().split("=")
            kwargs[key.strip()] = val.strip()

        # This is an entity to import
        elif not arg.startswith("--"):
            args.append(arg)
    return args, kwargs


def main(args, extra):
    try:
        importer = get_importer(args.import_type)
    except:
        sys.exit(f"{args.import_type} is not a known importer.")

    # Ensure support for --delim and --newline
    extra, kwargs = parse_extra(extra)

    results = importer.scrape(extra)
    print("Found %s results" % len(results))

    # If we have results and it's not a dry run, create the repos
    if results and not args.dry_run:
        importer.create(
            database=args.database, config_file=args.config_file, update=args.update
        )
