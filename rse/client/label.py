"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia


def main(args, extra):

    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    # Grab the repository uid, label key and value
    uid, key, value = args.values

    try:
        enc.label(uid=uid, key=key, value=value, force=args.force)
    except Exception as exc:
        print(exc)
