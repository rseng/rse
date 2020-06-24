"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
from rse.exceptions import RepoNotFoundError


def main(args, extra):

    # Create a research software encyclopedia
    client = Encyclopedia(config_file=args.config_file, database=args.database)

    # If a file is defined, we import from it
    if args.file is not None:
        try:
            if args.type[0] == "criteria":
                client.import_criteria_annotation(
                    input_file=args.file, username=args.username
                )
            elif args.type[0] == "taxonomy":
                client.import_taxonomy_annotation(
                    input_file=args.file, username=args.username
                )
        except Exception as exc:
            print(exc)

    # The type is either criteria or taxonomy
    else:
        try:
            client.annotate(
                username=args.username,
                atype=args.type[0],
                unseen_only=not args.all_repos,
                repo=args.repo,
                save=True,
            )
        except RepoNotFoundError as exc:
            print(exc)
