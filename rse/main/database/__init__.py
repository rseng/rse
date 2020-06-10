"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


def init_db(database, config_dir=None, database_string="", config=None):
    """Initialize the database, meaning a base client and appropriate functions
       to save, or generate a unique ID based on the backend being used. Each
       client has it's own init to check for a connection (or filesystem 
       path existence) and then functions to interact with entities.
    """
    # Case 1: Filesystem database saves to ./database
    if database == "filesystem":
        from .filesystem import FileSystemDatabase as Database

    # Case 2: Sqlite database saves to rse.db
    elif database.startswith("sqlite"):
        from .sqlite import SqliteDatabase as Database

    # Case 3: Postgresql or mysql+pymysql
    else:
        from .relational import RelationalDatabase as Database
    return Database(
        config_dir=config_dir,
        database_string=database_string,
        database=database,
        config=config,
    )
