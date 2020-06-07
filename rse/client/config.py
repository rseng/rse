"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.exceptions import DatabaseStringFormatError, MissingDatabaseString
from rse.main.config import Config
import logging
import os
import re


def main(args, extra):

    bot = logging.getLogger("rse.client")

    # The user wants to set the database
    if args.database:
        if not re.search("^(sqlite|filesystem|mysql+pymysql|postgres)", args.database):
            raise DatabaseStringFormatError

        # Ensure that database string, if exists, is correct
        database = args.database.split("://")[0]
        connection_string = args.database.replace(database, "", 1)

        # Instantiate a config with the correct configuration directory
        config = Config(config_file=args.config_file)

        # Update the database (not saved yet)
        config.update("DEFAULT", "database", database)

        # Mysql and postgres require connection strings
        if not connection_string and database in ["postgres", "mysql+pymysql"]:
            raise MissingDatabaseString(
                "You are required to provide a connection string for mysql+pymysql and postgres."
            )

        # Sqlite can be a path to a file, but must be located in root of config home
        elif connection_string and database == "sqlite":
            connection_string = os.path.basename(connection_string)

        # Connection string will be validated on init
        config.update("DEFAULT", "databaseConnect", connection_string)

        # If we make it here, save the configuration
        config.save()
        bot.info(f"Configuration saved with database {args.database}")

    # Set a value for a particular executor
    elif args.set:
        executor, key, value = args.set
        config = Config(config_dir=args.config_dir)
        executor = "executor.%s" % executor.lower()
        config.update(executor, key, value)
        config.save()
        bot.info(f"Configuration saved with {executor} {key} {value}")
