"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


class MissingEnvironmentVariable(RuntimeError):
    """Thrown if a required environment variable is not provided."""

    def __init__(self, varname, *args, **kwargs):
        super(MissingEnvironmentVariable, self).__init__(*args, **kwargs)
        self.varname = varname

    def __str__(self):
        return "Missing environment variable '{}' is required".format(self.varname)


class DirectoryNotFoundError(FileNotFoundError):
    """Thrown if a directory is not found"""

    def __init__(self, dirname, reason, *args, **kwargs):
        super(DirectoryNotFoundError, self).__init__(*args, **kwargs)
        self.dirname = dirname
        self.reason = reason

    def __str__(self):
        return "{} {}.".format(self.dirname, self.reason)


class MissingDatabaseString(RuntimeError):
    """Thrown if a database string is required and not provided"""

    def __init__(self, reason=None, *args, **kwargs):
        super(MissingDatabaseString, self).__init__(*args, **kwargs)
        self.reason = reason

    def __str__(self):
        return (
            self.reason
            or "A database url must be defined to use a relational database. Set with rse config --database"
        )


class DatabaseStringFormatError(RuntimeError):
    """Thrown if database prefix is not supported"""

    def __str__(self):
        return (
            "Database must start with sqlite, filesystem, mysql+pymysql, or postgres."
        )


## Repos


class RepoError(RuntimeError):
    """Abstract base class for any kind of RepoError."""

    def __init__(self, uid=None, reason=None, *args, **kwargs):
        super(RepoError, self).__init__(*args, **kwargs)
        self.uid = uid or ""
        self.reason = reason or "There was a problem with repository"

    def __str__(self):
        return "{} {}".format(self.reason, self.uid)


class MultipleReposExistError(RepoError):
    """Thrown if multiple repos exist."""

    def __init__(self, uid, *args, **kwargs):
        reason = "More than one repository found for"
        super(MultipleReposExistError, self).__init__(
            uid=uid, reason=reason, *args, **kwargs
        )


class RepoNotFoundError(RepoError):
    """Thrown if a repo does not exist (for a remote)"""

    def __init__(self, uid, *args, **kwargs):
        reason = "Cannot find repo"
        super(RepoNotFoundError, self).__init__(uid=uid, reason=reason, *args, **kwargs)


class NoReposError(RepoError):
    """Thrown if repos are requested, but there are none"""

    def __init__(self, *args, **kwargs):
        reason = "There are no repos in the database."
        super(NoReposError, self).__init__(reason=reason, *args, **kwargs)


class RepoMetadataExistError(RepoError):
    """Thrown if a metadata value (label) already exists."""

    def __init__(self, uid, key, *args, **kwargs):
        reason = "Metadata value %s already is defined." % key
        super(RepoMetadataExistError, self).__init__(
            uid=uid, reason=reason, *args, **kwargs
        )
