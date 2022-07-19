__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import os
import shutil
import re
import json

from rse.logger.message import bot
from rse.utils.file import write_file
from datetime import datetime

import logging

logger = logging.getLogger("rse.main")
here = os.path.abspath(os.path.dirname(__file__))

markdown_template = """---
%s
date: "%s"
---
"""


def get_exporter(name):
    """
    Get an exporter by name. Designed to support additional ones.
    """
    if name.lower() == "jekyll":
        return JekyllExporter
    bot.exit(f"Exporter {name} is not known.")


class Exporter:
    def __init__(self, path):
        self.path = os.path.abspath(path)


class JekyllExporter(Exporter):
    def export(self, repos):
        if not os.path.exists(self.path):
            template = os.path.join(here, "jekyll")
            shutil.copytree(template, self.path)

        # We will regenerate the software folder
        software_dir = os.path.join(self.path, "_software")
        if os.path.exists(software_dir):
            shutil.rmtree(software_dir)
        os.mkdir(software_dir)

        # Iterate through repos to generate data
        print("Generating jekyll web export")
        for repo in repos:

            # url will be over-written by jekyll templates, etc.
            if "url" in repo and repo["url"]:
                repo["repo_url"] = repo["url"]

            # Flatten data to be on one level
            if "data" in repo:
                for k, v in repo["data"].items():
                    if isinstance(v, str):
                        v = re.sub("(\n|\r)", " ", v)

                    # update repo to have one level of data on the top
                    if v:
                        repo[k] = v
                del repo["data"]

            # Render the "rest" as all key value pairs
            rest = ""
            for k, v in repo.items():
                if not isinstance(v, str):
                    rest += f"{k}: {json.dumps(v)}\n"
                else:
                    for char, replace in [('"', "")]:
                        v = v.replace(char, replace)
                    rest += f'{k}: "{v}"\n'

            template = markdown_template % (rest.strip("\n"), datetime.now())

            slug = repo["uid"].replace("/", "-")
            markdown_path = os.path.join(software_dir, "%s.md" % slug)
            write_file(template, markdown_path)
        print("Export is complete!")
