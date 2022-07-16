"""

Copyright (C) 2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from .base import ParserBase
import rse.defaults
import logging
import os
import re

bot = logging.getLogger("rse.main.parsers.custom")


class CustomParser(ParserBase):

    name = rse.defaults.RSE_CUSTOM_DATABASE_DIR
    matchstring = "custom"

    def __init__(self, uid=None, **kwargs):
        if "namespace" in kwargs:
            self.name = kwargs["namespace"]
        super().__init__(uid)

    def _set_uid(self, uid):
        """
        Set the uid
        """
        # Split by os sep and cleanup
        parts = []
        for part in uid.split(os.sep):
            parts.append(re.sub("[.: ]", "-", part).lower().strip("-"))
        return os.sep.join(parts)

    def set_metadata(self, **kwargs):
        for field in ["url", "title", "description"]:
            if field not in kwargs:
                bot.exit(f"Missing field {field} for custom parser {self.uid}")
            self.data[field] = kwargs[field]
        for key, value in kwargs.items():
            if key not in self.data:
                self.data[key] = value

    def get_url(self, data=None):
        data = data or self.data
        return data.get("url")

    def get_description(self, data=None):
        """
        a common function for a parser to return a description.
        """
        data = data or self.data
        return data.get("description")

    def get_metadata(self, uri=None):
        return self.data
