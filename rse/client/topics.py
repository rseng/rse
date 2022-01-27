"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia


def main(args, extra):

    # Create an encyclopedia object
    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    # Does the user want to search for repos with one or more topics?
    if not args.search:
        topics = enc.topics(pattern=args.pattern)
        print("\n".join(topics))
    else:
        repos = enc.repos_by_topics(topics=args.search)
        print("\n".join(repos))
