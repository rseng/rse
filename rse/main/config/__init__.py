"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import configparser
import logging
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))

bot = logging.getLogger("rse.main.config")


class Config:
    def __init__(self, config_file="rse.ini", load=True, generate=False):
        """Controller for an rse.ini config file."""
        self.configfile = os.path.abspath(config_file)

        # If the config file doesn't exist, generate it
        if not os.path.exists(self.configfile):
            if generate:
                default_config = os.path.join(here, "config.ini")
                bot.info(
                    "Generating configuration file %s"
                    % os.path.basename(self.configfile)
                )
                shutil.copyfile(default_config, self.configfile)
            else:
                sys.exit(
                    "rse.ini not found, specify with --config_file or move to directory."
                )

        # Load the config file if wanted
        if load and os.path.exists(self.configfile):
            self.read()

    def get(self, section, key):
        """A wrapper to config.get to directly interact with the self.config"""
        return self.config.get(section, key)

    def update(self, section, key, value, save=False):
        """update client secrets will update the data structure for a particular
        authentication. This should only be used for a (quasi permanent) token
        or similar. The secrets file, if found, is updated and saved by default.
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

        # If save is true (to persist settings)
        if save:
            self.save()

    def save(self):
        """save configuration back to it's original file"""
        with open(self.configfile, "w") as configfile:
            self.config.write(configfile)

    def read(self, configfile=None):
        """read in configuration file. By default use self.configfile."""
        configfile = configfile or self.configfile
        config = configparser.ConfigParser()
        config.read(configfile)
        self.config = config
