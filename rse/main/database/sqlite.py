"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main.database.relational import RelationalDatabase

import logging
import os

bot = logging.getLogger("rse.main.database.sqlite")


class SqliteDatabase(RelationalDatabase):
    """A SqliteDatabase writes to a rse.db file in $HOME/.rse. This is
       the suggested database backend for QueueMe, as it doesn't require anything
       beyond a filesystem and still allows for relational type queries.
    """

    database = "sqlite"

    def __init__(self, config_dir, config=None, **kwargs):
        """init for the filesystem ensures that the base folder (named 
           according to the studyid) exists.
        """
        database_file = kwargs.get("database_string", "rse.db") or "rse.db"

        # Derive database path, use default of rse.db if not provided
        db_path = os.path.join(config_dir, database_file)
        if not db_path.endswith(".db"):
            raise RuntimeError(f"Invalid database filename {database_file}")

        self.config = config
        self.db = "sqlite:///%s" % db_path
        self.create_database()
