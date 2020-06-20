"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
import sys


def main(args, extra):

    # Create a research software encyclopedia
    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    # A uid is required here
    if not args.uid and not args.file:
        sys.exit("Please provide a software identifier or file to add.")

    # If a file is provided, add in bulk (skips over those already present)
    if args.file:
        enc.bulk_add(args.file)
    else:
        enc.add(args.uid)
