---
title: Research Software
permalink: /
---

> What is rse?

The research software encyclopedia (rse) is a collection of tools and interfaces
to support management, query, and understand of research software. The library
is intended to create value for the community of research software engineers, namely
by providing a tool for management and introspection of research software.
The rse is intended for research software engineers, funding bodies, or other
invested parties of interest to be able to better qualify and quantify research
software engineering work. The rse considers the source code the ultimate source of truth.
This means creating namespaces of software repositories (e.g., GitHub, GitLab) 
and then providing automated ways to parse these repositories to extract metadata,
and prompt interested parties to answer questions about the software with respect
to it's qualities and grouping. We want to do this to:

 - create a database of research software that is easy to search and discuss
 - help evaluate each software repository for a set of criteria
 - organize the database entries into a taxonomy of research software

and then to use the criteria and taxonomy to derive a context-specific
[definition of research software](https://docs.google.com/document/u/1/d/1wDb0udH9OrFWrMBsAVb8RrUMCKKRHoyEep7yveJ1d0k/edit).


<a id="how-is-it-deployed">
> How is the rse deployed?

The rse uses the following resources:

 - [rseng/rseng](https://rseng.github.io/rseng/): serves the taxonomy and criteria
 - [rseng/software](https://github.com/rseng/software): is a static (flat file) "database" that is updated automatically.

Unlike traditional software databases, the rse and supporting tools are completely
hosted and automated without need to manage a server.
The rse works by way of regularly scraping known research software databases,
and then adding entries to [rseng/software](https://github.com/rseng/software).
Users are then (also automatically) prompted to answer questions about criteria
and taxonomy via social media and chat (not developed yet).  Non-traditional
use cases for the rse are generating a static web-site of your own research 
software! See [the tutorials](https://rseng.github.io/rseng/blog/) section of the 
criteria and taxonomy site to get started.


<a id="how-does-it-work">
> How does it work?

After you [install]({{ site.baseurl }}/install/) rse, you might first want to
create a local database, or a folder that has software repositories on the filesystem
or a relational database.

```bash
$ rse init .
```

More likely you want to clone an existing research software encyclopedia, to
update, annotate, or otherwise interact with.

```bash
git clone https://github.com/rseng/software
cd software
```

And then proceed to add, list, update, annotate, etc. See the [commands]({{ site.baseurl }}/getting-started/commands/)
section to get started.

<a id="what-is-a-parser">
> What is a parser?

A parser is a class within the research software encyclopedia that is optimized to parse a specific kind of
repository. When you create a local software respository, you are interacting with
an [Encyclopedia](https://github.com/rseng/rse/blob/master/rse/main/__init__.py#L32) 
class that acts as a controller for different kinds
of uris. However, you can also interact with a parser on it's own, in the
case that you want to do your own analysis of research software outside
of the rse software repository structure.

```python
from rse.main.parsers import GitHubParser
parser = GitHubParser("github.com/vsoch/salad")
```

The interactive session means opening up a web interface that shows an interactive
table that updates automatically with changed or new tasks via web sockets.

<a id="use-cases">
> What are intended use cases for rse?

The research sofware encyclopedia is intended to help manage and query a database
of research software, and then filter for different use cases or contexts. Example
use cases are the following:

 - assessing software for popularity or usage
 - deriving a custom set based on criteria or place in a taxonomy
 - exporting metrics for a custom analysis
 - a common interface to multiple sources of software (e.g., export from JoSS)

More specifically, it's very likely that a definition of research software can
vary based on different contexts and use cases. The rse provide a simple method
to answer questions, or filter to groups, in order to answer the question
"Is it research software?"

<a id="where-do-i-go">
> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page,
which has links for getting started with creating or interacting with a software database,
and assessing criteria.
