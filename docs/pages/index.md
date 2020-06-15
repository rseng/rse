---
title: Research Software
permalink: /
---

> What is rse?

The research software encyclopedia (rse) is a collection of tools and interfaces
to support management, query, and understand of research software. The library
is intended to create value for the community of research software engineers, namely
by providing a tool for management and introspection of research software.
This means creating namespaces of software repositories (for example, GitHub would
have a namespace of GitHub urls) and then providing automated ways to parse these
repositories to extract metadata. The reason we want metadata is to:

 - create a database of research software that is easy to search and discuss
 - help evaluate each software repository for a set of criteria
 - organize the database entries into a taxonomy of research software

and then to use the criteria and taxonomy to derive a context-specific
[definition of research software](https://docs.google.com/document/u/1/d/1wDb0udH9OrFWrMBsAVb8RrUMCKKRHoyEep7yveJ1d0k/edit).

<a id="#how-does-it-work">
> How does it work?

After you [install]({{ site.baseurl }}/install/) rse, you might first want to
create a local database, or a folder that has software repositories on the filesystem
or a relational database.

```bash
$ rse init .
```

> What is a parser?

A parser is a class within the research software encyclopedia that is optimized to parse a specific kind of
repository. When you create a local software respository, you are interacting with
a [Encyclopedia]() class that acts as a controller for different kinds
of uris. However, you can also interact with a parser on it's own, in the
case that you want to do your own analysis of research software outside
of the rse software repository structure.

```python
from rse.main.parsers import GitHubParser
parser = GitHubParser("github.com/vsoch/salad")
```

The interactive session means opening up a web interface that shows an interactive
table that updates automatically with changed or new tasks via web sockets.

> What are intended use cases for rse?

The research sofware encyclopedia is intended to help manage and query a database
of research software, and then filter for different use cases or contexts. Example
use cases are the following:

 - assessing software for popularity or usage
 - deriving a custom set based on criteria or place in a taxonomy
 - exporting metrics for a custom analysis
 - a common interface to multiple sources of software (e.g., export from JoSS)

More specifically, rse provides a layer of reproducibility to your terminal usage,
because instead of spitting out commands that you do not remember or doing a grep
to search your linux history, you instead store the commands in a database.
The commands are parsed to matched executors of interest (e.g. slurm would
match srun and expose commands to interact with your submission) and if no executor is matched,
it's treated as a standard Shell command (shell capture standard output, error, and return codes).

> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page,
which has links for getting started with creating or interacting with a software database,
and assessing criteria.
