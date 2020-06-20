"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Encyclopedia
from rse.exceptions import RepoNotFoundError, NoReposError
import json
import logging

bot = logging.getLogger("rse.client")


def main(args, extra):

    # Create a research software encyclopedia
    enc = Encyclopedia(config_file=args.config_file, database=args.database)

    try:
        repo = enc.get(args.uid)
        print(json.dumps(repo.load(), indent=4))
    except NoReposError:
        bot.error(
            "There are no software repositories in the database! Use rse add to add some."
        )
    except RepoNotFoundError:
        bot.error(f"{args.uid} does not exist in the database. Use rse add to add it.")
