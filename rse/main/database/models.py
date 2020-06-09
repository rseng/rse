"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import json


try:
    from sqlalchemy import Column, DateTime, String, Text, func
    from sqlalchemy.ext.declarative import declarative_base
except:
    raise ImportError("sqlalchemy", "is required for a non-filesystem database.")

# Shared declarative base
Base = declarative_base()


class SoftwareRepository(Base):
    """A software repository.
    """

    __tablename__ = "software_repository"
    uid = Column(String(150), primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    parser_name = Column(String(50))
    data = Column(Text, nullable=True)

    def __init__(self, uid=None, parser=None, data={}):
        self.uid = uid
        self.parser_name = parser
        self.data = data

    def summary(self):
        return self.parser.summary()

    def load(self):
        """loading a software repository means exporting as json"""
        data = {"parser": self.parser_name, "uid": self.uid, "data": {}}

        if self.data:
            data["data"] = json.loads(self.data)

        return data

    def export(self):
        """Export removes the outer wrapper, and just returns the data"""
        return self.load().get("data", {})

    def __repr__(self):
        return "<SoftwareRepository %r>" % self.uid
