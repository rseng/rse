"""

Copyright (C) 2020-2023 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import logging
import os
from multiprocessing import Process

from rse.main import Encyclopedia
from rse.utils.file import write_file

bot = logging.getLogger("rse.client")


def main(args, extra):
    client = Encyclopedia(config_file=args.config_file, database=args.database)

    # Case 1: empty list indicates listing all
    if os.path.exists(args.path) and not args.force:
        bot.error(f"{args.path} already exists, use --force to overwrite it.")

    # Export a list of repos
    if args.export_type == "repos-txt":
        # We just want the unique id, the first result
        repos = [x[0] for x in client.list()]
        write_file("\n".join(repos), args.path)
        bot.info(f"Wrote {len(repos)} to {args.path}")

    # Static jekyll site (no annotation)
    elif args.export_type == "jekyll-web":
        client.export(args.path)

    # Static web export from flask to a directory
    elif args.export_type == "static-web":
        from rse.app.export import export_web_static
        from rse.app.server import start

        # Start the webserver on a separate process
        p = Process(
            target=start,  # port, debug, client, host, log-level, disable_annotate
            args=(args.port, args.debug, client, args.host, args.log_level, True),
        )
        p.start()

        # Do the export!
        export_web_static(
            export_dir=args.path,
            base_url="http://%s:%s" % (args.host, args.port),
            force=args.force,
            client=client,
            p=p,
        )

        # Ensure that it stops!
        p.kill()
