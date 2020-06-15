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

### Setup

 - [Configuration](configure/) your rse install, for example, choosing a database backend.
 - [Environment](environment/) variables can be set to control functionality.

### Usage

 - [Commands](commands/) including run, re-run, list (ls), get, and others.
 - [Parsers](parsers/) know how to parse some remote software repository
 - Dashboard: an annotation interface for criteria and taxonomy (under development)
 - [Containers](containers/) for pre-built environments to use rse.

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
                                  +-->+ other |
                                      |       |
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

**dashboard**

Is a Flask application that comes with rse, exposed via `rse start`, that provides
an table to manage and otherwise interact with tasks.

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

## Licenses

This code is licensed under the Mozilla, version 2.0 or later LICENSE.

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
