"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia


def main(args, extra):

    # Create a queue object, run the command to match to an executor
    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    # If a file is provided:
    if args.file:
        enc.bulk_update(args.file)
    else:
        enc.update(args.uid)
