"""

Copyright (C) 2020-2022 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import json

from rse.main import Encyclopedia
from rse.logger.message import bot


def analyze(args, extra):
    """analyze is intended to provide calculations for repos, by default including
    all taxonomy categories and criteria. For a custom set, the user should
    interact with the client directly.
    """
    client = Encyclopedia(config_file=args.config_file, database=args.database)
    result = client.analyze(repo=args.repo, cthresh=args.cthresh, tthresh=args.tthresh)

    # Create rows for criteria and taxonomy
    clookup = {c["uid"]: c for c in client.list_criteria()}
    tlookup = {t["uid"]: t for t in client.list_taxonomy()}
    crows = [
        [response, clookup[uid]["name"]] for uid, response in result["criteria"].items()
    ]
    trows = [
        [str(count), tlookup[uid]["name"]] for uid, count in result["taxonomy"].items()
    ]

    bot.info(f"Summary for {result['repo']}")
    bot.info("\nCriteria")
    bot.table(crows)
    bot.info("\nTaxonomy")
    bot.table(trows)


def summary(args, extra):
    """summary will return general counts for taxonomy, criteria, and users"""

    client = Encyclopedia(config_file=args.config_file, database=args.database)
    metrics = client.summary(args.repo)

    # Export only taxonomy metrics
    if args.metric_type == "taxonomy":
        updated = {}
        for field in ["taxonomy", "taxonomy-count", "repos"]:
            updated[field] = metrics[field]
        metrics = updated

    # Export only criteria metrics
    elif args.metric_type == "criteria":
        updated = {}
        for field in ["criteria", "criteria-count", "repos"]:
            updated[field] = metrics[field]
        metrics = updated

    # Export only user metrics
    elif args.metric_type == "users":
        updated = {}
        for field in ["users-count", "users", "repos"]:
            updated[field] = metrics[field]
        metrics = updated

    # Print metrics as json or table
    if metrics:
        print(json.dumps(metrics, indent=4))
