"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
import sys


def main(args, extra):

    # Clear a parser, uid, or target
    enc = Encyclopedia(config_file=args.config_file)

    # Pass the encyclopedia object to start a server
    # try:
    from rse.app.server import start

    start(port=args.port, client=enc, debug=args.debug, level=args.log_level)
    # except:
    #    sys.exit(
    #        "You must 'pip install rse[app]' 'pip install rse[all]' to use the dashboard."
    #    )
