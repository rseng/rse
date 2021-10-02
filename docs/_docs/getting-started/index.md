---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---

You should first [install]({{ site.baseurl }}/install/) rse.
This will place the executable `rse` in your bin folder, which is the client
for searching software, starting the interface, or otherwise interacting with
your software repository.

## Getting Started

### Introduction

 - [How does it work?](#how-does-it-work): How does rse work?
 - [Concepts](#concepts): What are common rse concepts?
 - [Quick Start](#quick-start): to install, create, and add software to an RSEPedia database.

### Setup

 - [Configuration](configure/) your rse install, for example, choosing a database backend.
 - [Environment](environment/) variables can be set to control functionality.

### Usage

 - [Commands](commands/) including run, re-run, list (ls), get, and others.
 - [Parsers](parsers/) know how to parse some remote software repository
 - [Scrapers](scrapers/) discover new software repositories via resource APIs.
 - [Dashboard](dashboard/): an annotation interface for criteria and taxonomy
 - [Containers](containers/) for pre-built environments to use rse.
 - [API](api/) application programming interface to expose software, criteria, and taxonomy
 - [Annotation](annotation/) of criteria and taxonomy items for research software

<a id="#how-does-it-work">
### How does it work?

As we've [mentioned]({{ site.baseurl }}/index.html), the research software encyclopedia
is intended to provide a database for you to manage and assess research software.
The interaction looks like the following:

```
                                      +--------+
                                      |        |
                                  +-->+ zenodo |
                                  |   |        |
                                  |   +--------+                    +--> rse update...
                                  |                                 |
+--------------+    +--------+    |   +--------+    +------------+  +--> rse get...
|              |    |        |    |   |        |    |            |  |
|  rse get...  +--->+ parser +------->+ github |--->| database   +--+--> rse ls...
|              |    |        |    |   |        |    |            |  |
+--------------+    +--------+    |   +--------+    +------------+  +--> rse search...
                                  |       .                         |
                                  |       .                         +--> rse exists...
                                  |   +-------+                     |
                                  |   |       |                     +--> rse start...
                                  +-->+ other |                     |
                                      |       |                     +--> rse annotate...
                                      +-------+

```

In the above diagram, we start with a rse get command, where we provide a namespaced 
identifier (e.g., `github.com/user/repository`) and it get's parsed by a particular
parser (e.g., github, or zenodo). The parser interacts with our database of choice
(filesystem, sqlite, mysql, or postgres) to save custom metadata for the repository,
which minimally includes a timestamp it was obtained and a url for it. The
user can then query rse to get, list, update, or export a set of software or a particular
repository. There is also an interactive web interface to do the same.

<a id="#concepts">
### Concepts

The following concepts might not be specific to rse, but are defined as the following
in the context of rse:

**parser**

A parser is a controller to handle taking a uri (unique resource identifier) and returning
metadata about the software. Minimally, a url is required to direct a user where to inspect it.
The Research Software Encyclopedia uses a set of base parsers (version
control systems) as sources of truth, and also provides additional parsers for the
user to interact with if desired (e.g., Zenodo).

**scraper**

A scraper is intended to run at some regular interface to update the research
software encyclopedia with entries from some external resource.

**dashboard**

Is a Flask application that comes with rse, exposed via `rse start`, that provides
an table to manage and otherwise interact with tasks.

**annotation**

Is the process of answering questions about one or more repositories in a software
encyclopedia, and also indicating category membership. This can be done interactively
in a web interface (under development) or via the command line.

**database**

A database is the backend database used by the research software encyclopedia to keep track
of your software. The default (and dummy)
database is the filesystem. If you want to use a different database backend then you need
to install the sqlachemy database dependency and then specify using 
sqlite for your configuration by doing the following:

```bash
$ pip install -e .[all]         # local install from repository
$ pip install -e rse[all]       # install from pypi
$ rse config --database sqlite
```

<a id="#quick-start">
## Quick Start

A quick example of installing the software and creating a database of research software with two entries from GitHub might look like the following:

```bash
$ pip install rse[all]
$ rse init
$ rse add https://github.com/citation-file-format/cff-converter-python
$ rse ls
1  github/citation-file-format/cff-converter-python
$ rse add https://gitlab.com/jspaaks/howfairis-livetest
$ rse ls
1  github/citation-file-format/cff-converter-python
2  gitlab/jspaaks/howfairis-livetest
$ tree database
database
├── github
│   └── citation-file-format
│       └── cff-converter-python
│           └── metadata.json
└── gitlab
    └── jspaaks
        └── howfairis-livetest
            └── metadata.json
$ cat database/github/citation-file-format/cff-converter-python/metadata.json 
```

And then you might want to look at [Annotation](annotation/) or criteria or taxonomy items,
[Scrapers](scrapers/) to automate adding software to your database, or generating
a [Dashboard](dashboard/) for others to explore.

## Licenses

This code is licensed under the Mozilla, version 2.0 or later LICENSE.

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
