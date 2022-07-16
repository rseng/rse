"""

Copyright (C) 2020-2022 Vanessa Sochat.

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
    """
    A software repository.
    """

    __tablename__ = "software_repository"
    uid = Column(String(150), primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    parser_name = Column(String(50))
    data = Column(Text, nullable=True)
    taxonomy = Column(Text, nullable=True)
    criteria = Column(Text, nullable=True)

    def __init__(self, uid=None, parser=None, data={}):
        self.uid = uid
        self.parser_name = parser
        self.data = data

    def summary(self):
        return self.parser.summary()

    @property
    def url(self):
        data = json.loads(self.data)
        return self.parser.get_url(data)

    @property
    def avatar(self):
        data = json.loads(self.data)
        return self.parser.get_avatar(data)

    @property
    def description(self):
        data = json.loads(self.data)
        return self.parser.get_description(data)

    def load(self):
        """
        loading a software repository means exporting as json
        """
        data = {"parser": self.parser_name, "uid": self.uid, "data": {}}

        if self.data:
            data["data"] = json.loads(self.data)

        return data

    def get_criteria(self):
        """
        load criteria into a dictionary
        """
        return json.loads(self.criteria or "{}")

    def get_taxonomy(self):
        """
        load taxonomy into a dictionary
        """
        return json.loads(self.taxonomy or "{}")

    def update_criteria(self, uid, username, response):
        """
        Given a username and unique id update criteria
        """
        criteria = self.get_criteria()

        if uid not in criteria:
            criteria[uid] = {}
        if response:
            criteria[uid][username] = response
            self.criteria = json.dumps(criteria)

    def update_taxonomy(self, username, uids):
        """
        Given a username and unique id update taxonomy items
        """
        taxonomy = self.get_taxonomy()

        if username not in taxonomy:
            taxonomy[username] = uids
        self.taxonomy = json.dumps(taxonomy)

    def export(self):
        """
        Export removes the outer wrapper, and just returns the data
        """
        return self.load().get("data", {})

    def __repr__(self):
        return "<SoftwareRepository %r>" % self.uid

    # Annotation

    def has_criteria_annotation(self, uid, username):
        """
        Determine if a repository has been annotated by a user.
        """
        if not self.criteria:
            return False
        criteria = json.loads(self.criteria)
        if uid not in criteria:
            return False
        if username not in criteria[uid].get("users", []):
            return False
        return True

    def has_taxonomy_annotation(self, username):
        """
        Determine if a repository has been annotated by a user.
        """
        if not self.taxonomy:
            return False
        taxonomy = json.loads(self.taxonomy)
        if username not in taxonomy:
            return False
        return True
