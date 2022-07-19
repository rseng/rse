"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.file import read_file

from datetime import datetime
import copy
import os
import json
import tempfile
import subprocess


class Capturing:
    """
    capture output from stdout and stderr into capture object.
    This is based off of github.com/vsoch/gridtest but modified
    to write files. The stderr and stdout are set to temporary files at
    the init of the capture, and then they are closed when we exit. This
    means expected usage looks like:

    with Capturing() as capture:
        process = subprocess.Popen(...)

    And then the output and error are retrieved from reading the files:
    and exposed as properties to the client:

        capture.out
        capture.err

    And cleanup means deleting these files, if they exist.
    """

    def __enter__(self):
        self.set_stdout()
        self.set_stderr()
        self.output = []
        self.error = []
        return self

    def set_stdout(self):
        self.stdout = open(tempfile.mkstemp()[1], "w")

    def set_stderr(self):
        self.stderr = open(tempfile.mkstemp()[1], "w")

    def __exit__(self, *args):
        self.stderr.close()
        self.stdout.close()

    @property
    def out(self):
        """Return output stream. Returns empty string if empty or doesn't exist.
        Returns (str) : output stream written to file
        """
        if os.path.exists(self.stdout.name):
            return read_file(self.stdout.name)
        return ""

    @property
    def err(self):
        """
        Return error stream. Returns empty string if empty or doesn't exist.
        Returns (str) : error stream written to file
        """
        if os.path.exists(self.stderr.name):
            return read_file(self.stderr.name)
        return ""

    def cleanup(self):
        for filename in [self.stdout.name, self.stderr.name]:
            if os.path.exists(filename):
                os.remove(filename)


class ParserBase:
    """
    A parser base exists to extract and format repository metadata.
    """

    name = "base"

    def __init__(self, uid=None, **kwargs):
        """
        set a unique id that includes parser name (type) and unique identifier)
        """
        self.uid = None
        if uid is not None:
            self.set_uid(uid)
        if not hasattr(self, "data"):
            self.data = {}

    def set_uid(self, uid):
        """
        Given a unique resource identifier, set it for the parser
        """
        uid = self._set_uid(uid)
        if not uid.startswith(self.name):
            uid = "%s%s%s" % (self.name, os.sep, uid)
        self.uid = uid

    def _set_uid(self, uid):
        """Given a uri from the user, parse the consistent identifier (e.g.,
        in the case of GitHub a repository username and name)
        """
        raise NotImplementedError

    def load(self, data):
        """
        If a repository has already been instantiated, we might want to load
        data into a parser to interact with it
        """
        if isinstance(data, str):
            data = json.loads(data)
        self.data = data

    def _export_common(self):
        """
        export common repo variables such as timestamp when it was updated,
        and we try to add the common variables like description, etc.
        """
        res = {"timestamp": str(datetime.now())}
        for field in ["description", "avatar", "url"]:
            try:
                # If we load again, "data" will be a field (the automated data from the parser)
                func = getattr(self, f"get_{field}")
                res[field] = func(self.data) or func(self.data.get("data"))
            except:
                pass
        return res

    def get_url(self, data):
        """
        a common function for a parser to return the html url for the
        upper level of metadata
        """
        raise NotImplementedError

    def get_avatar(self, data=None):
        data = data or self.data
        return data.get("avatar")

    def get_description(self, data):
        """
        a common function for a parser to return a description.
        """
        raise NotImplementedError

    def export(self):
        """
        return data as json. This is intended to save to the software database.
        Any important parser specific metadata should be added to self.data
        """
        # Get common context (e.g., pwd)
        data = copy.deepcopy(self.data)
        for k, v in self._export_common().items():
            if v:
                data[k] = v
        return data

    def get_metadata(self, uri, **kwargs):
        """
        The get_metadata function should take a general URI for a parser
        and populate the self.data
        """
        raise NotImplementedError

    def capture(self, cmd):
        """
        capture is a helper function to capture a shell command. We
        use Capturing and then save attributes like the pid, output, error
        to it, and return to the calling function. For example:

        capture = self.capture_command(cmd)
        self.pid = capture.pid
        self.returncode = capture.returncode
        self.out = capture.output
        self.err = capture.error
        """
        # Capturing provides temporary output and error files
        with Capturing() as capture:
            process = subprocess.Popen(
                cmd,
                stdout=capture.stdout,
                stderr=capture.stderr,
                universal_newlines=True,
            )
            capture.pid = process.pid
            returncode = process.poll()

            # Iterate through the output
            while returncode is None:
                returncode = process.poll()

        # Get the remainder of lines, add return code
        capture.output += [x for x in self.decode(capture.out) if x]
        capture.error += [x for x in self.decode(capture.err) if x]

        # Cleanup capture files and save final return code
        capture.cleanup()
        capture.returncode = returncode
        return capture

    def get_setting(self, key, default=None):
        """
        Get a setting, meaning that we first check the environment, then
        the config file, and then (if provided) a default.
        """
        # First preference to environment
        envar = ("RSE_%s_%s" % (self.name, key)).upper()
        envar = os.environ.get(envar)
        if envar is not None:
            return envar

        # Next preference to config setting
        parser = "parser.%s" % self.name

        # Parsers instantiated separate from database won't have config
        if not hasattr(self, "config") or not self.config:
            return default
        if parser not in self.config.config:
            return default
        if key in self.config.config[parser]:
            return self.config.get(parser, key)
        return default

    def summary(self):
        if self.uid:
            return "[%s][%s]" % (self.name, self.uid)
        return "[%s]" % self.name
