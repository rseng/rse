"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.utils.urls import get_user_agent
from rse.utils.file import mkdir_p, write_file, write_json
from rse.defaults import RSE_URL_PREFIX
import json
import logging
import os
import requests
import shutil
import sys
import time

here = os.path.abspath(os.path.dirname(__file__))

bot = logging.getLogger("rse.app.export")


def export_web_static(export_dir, base_url, client, force=False):
    """
    Export a running web interface to a folder. If the folder exists, the
    user must use force. This should be run via:
        rse export --type static-web [export_dir]
    If the user manually starts the server, the user needs to do:
        export RSE_DISABLE_ANNOTATE=True before the server is started
    to disable the annotation interface button. This will be fixed
    in a future PR to have an interface that submits an issue to do
    an annotation, but this needs to be developed first.

    Arguments:
     - export_dir (str)      : the path to an export directory
     - base_url (str)        : the base url of the server, including port
     - client (Encyclopedia) : the encyclopedia to use
     - force (bool)          : if directory exists, overwrite
    """
    print(f"Starting export for {base_url}")
    time.sleep(2)

    # Ensure that the server is running
    try:
        requests.head(base_url).status_code == 200
    except:
        bot.info(
            "Please export after the server is running: export --type static-web [export_dir]"
        )
        return

    # Output directory cannot exist if force
    if os.path.exists(export_dir) and not force:
        sys.exit(f"{export_dir} exists, use --force to overwrite.")

    # Create export directory if it doesn't exist
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)

    # Copy static files
    static_files = os.path.join(export_dir, "static")
    if not os.path.exists(static_files):
        shutil.copytree(os.path.join(here, "static"), static_files)

    # Prepare urls (and filepath relative to export_dir) for export
    urls = {base_url: "index.html"}

    # Create static data export
    data = []

    # Add repos and static annotation
    for repo in client.list():
        repo = client.get(repo[0])
        repo_path = os.path.join("repository", repo.uid)

        if isinstance(repo.data, str):
            repo.data = json.loads(data)

        # Get the list of topics
        topiclist = repo.data.get("topics", []) or repo.data.get("data", {}).get(
            "topics", []
        )
        data.append(
            {
                "uid": repo.uid,
                "url": repo.url,
                "rel": "%s%s" % (RSE_URL_PREFIX, repo_path),
                "avatar": repo.avatar,
                "description": repo.description,
                "topics": topiclist,
            }
        )
        # Currently don't link to repository page
        # urls["%s%s%s" % (base_url, RSE_URL_PREFIX, repo_path)] = os.path.join(
        #    repo_path, "index.html"
        # )

        # Static annotation endpoints
        for annotation_type in ["criteria", "taxonomy"]:
            urls[
                "%s%s%s/annotate-%s"
                % (base_url, RSE_URL_PREFIX, repo_path, annotation_type)
            ] = os.path.join(repo_path, "annotate-%s" % annotation_type, "index.html")

        # Repository API endpoints
        urls["%s%sapi/repos/%s" % (base_url, RSE_URL_PREFIX, repo.uid)] = os.path.join(
            "api", "repos", repo.uid, "index.json"
        )

    # Add API endpoints
    urls["%s%sapi" % (base_url, RSE_URL_PREFIX)] = os.path.join("api", "index.json")
    urls["%s%sapi/repos" % (base_url, RSE_URL_PREFIX)] = os.path.join(
        "api", "repos", "index.json"
    )

    for parser in ["github", "gitlab"]:
        urls[
            "%s%sapi/repos/parser/%s" % (base_url, RSE_URL_PREFIX, parser)
        ] = os.path.join("api", "repos", "parser", parser, "index.json")

    urls["%s%sapi/taxonomy" % (base_url, RSE_URL_PREFIX)] = os.path.join(
        "api", "taxonomy", "index.json"
    )
    urls["%s%sapi/criteria" % (base_url, RSE_URL_PREFIX)] = os.path.join(
        "api", "criteria", "index.json"
    )

    # Add search, criteria, and taxonomy
    for term in ["search", "criteria", "taxonomy"]:
        urls["%s%s%s" % (base_url, RSE_URL_PREFIX, term)] = os.path.join(
            term, "index.html"
        )

    for url, outfile in urls.items():

        # Skip if we've already created it
        if os.path.exists(outfile):
            continue

        # Update the output file with the repository
        outfile = os.path.join(export_dir, outfile)

        # Create nested output folder, if doesn't exist
        out_dir = os.path.dirname(outfile)
        if not os.path.exists(out_dir):
            mkdir_p(out_dir)

        # Url might have a prefix
        response = requests.get(url, headers={"User-Agent": get_user_agent()})
        if response.status_code == 200:
            write_file(response.text, outfile)
        else:
            print(f"Issue parsing {url}")

    print("Generating data export")
    write_json(data, os.path.join(export_dir, "data.json"))
    print("Export is complete!")
