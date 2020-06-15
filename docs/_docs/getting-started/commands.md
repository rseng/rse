---
title: Commands
category: Getting Started
permalink: /getting-started/commands/index.html
order: 3
---

This section includes commands for the Research Software Encyclopedia, specifically
to interact with a software repository that further can control parsers and update
your software database.

 - [Exists](#exists): determine if a particular repository exists in your local repository
 - [Add](#add): add a new software repository to your database
 - [Get](#get): retrieve current metadata for a piece of software, or all software
 - [Update](#update): update metadata for a single repository or all repositories
 - [List](#list) all software or software specific to a parser

 - [Remote](#remote): query the rseng/software remote database
 - [Clear](#clear) a software repository, all under a parser, or the entire database.
 - [Search](#search) across your software to find a particular one.
 - [Shell](#shell) into a Python shell to interact with an encyclopedia client.
 - [Start](#start) an interactive dashboard to see software and annotate crtieria and taxonomy membership.


<a id="exists">
## Exists

If you are working locally, the first thing you might want to do is determine if
a particular software repository exists in your database. You can thus do:

```bash
$ rse exists github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
github.com/singularityhub/sregistry does not exist.
```

This assumes the rse.ini config file is in the present working directory. If not,
you should specify it:

```bash
$ rse --config_file ../software/rse.ini exists github.com/singularityhub/sregistry
```

<a id="add">
## Add

Let's say that we tested if our software of interest existed in the repository,
and then we found that it did not, and want to add it. We can use `rse add`
to do this.

```bash
$ rse --config_file ../software/rse.ini add github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
INFO:rse.main:github.com/singularityhub/sregistry was added to the the database.
```

If the entry already exists, you will be told that!

```bash
$ rse add github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
ERROR:rse.main:github.com/singularityhub/sregistry already exists in the database.
```

And if the entry doesn't exist on the remote (e.g., GitHub) you'll see:

```bash
$ rse add github.com/singularityhub/singularity
INFO:rse.main:Database: filesystem
ERROR:rse.main.parsers.github:Cannot find repository singularityhub/singularity.
```

We can also add in bulk from a text file with one repository per line. For
example, here is a small one:

```
github.com/stan-dev/stan
github.com/mathjax/MathJax
github.com/optuna/optuna
github.com/PyTables/PyTables
```

We would add in bulk as follows:

```bash
$ rse add --file repos.txt
```

By default, repos that are already added will be skipped over.

<a id="get">
## Get 

A get will retrieve a known identifier. Unlike exists, if it doesn't exist, it will
parse and retrieve it for you.

```bash
$ rse get github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
{
    "parser": "github",
    "uid": "github/singularityhub/sregistry",
    "data": {
        "timestamp": "2020-06-07 14:00:24.727142",
        "url": "https://api.github.com/repos/singularityhub/sregistry",
        "id": 99180575,
        "node_id": "MDEwOlJlcG9zaXRvcnk5OTE4MDU3NQ==",
        "name": "sregistry",
...
        "network_count": 32,
        "subscribers_count": 10
    }
}
```

If you run get without an argument, it will retrieve the last modified entry
for you:

```bash
rse get
```

<a id="update">
## Update

Updating an entry coincides with retriving updated metadata. You can do this
for an existing software repository:

```bash
$ rse update github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
INFO:rse.main:github/singularityhub/sregistry has been updated.
```

And of course you cannot update an entry that doesn't exist.

```bash
$ rse update github.com/singularityhub/doesnotexist
INFO:rse.main:Database: filesystem
ERROR:rse.main:github.com/singularityhub/doesnotexist does not exist.
```

We can also update in bulk from a text file with one repository per line. For
example, here is a small one:

```
github.com/stan-dev/stan
github.com/mathjax/MathJax
github.com/optuna/optuna
github.com/PyTables/PyTables
```

We would update in bulk as follows:

```bash
$ rse update --file repos.txt
```

By default, repos that are not present will be skipped over.

<a id="list">
## List

For the command line, you can easily list repos. For the filesystem database,
since we would need to read in several json files, the listing just shows the
repo ids. If you do a general list with `rse ls`, it will show all software ids:

```bash
$ rse ls
DATABASE: filesystem
INFO:rse.main:Database: filesystem
1  github/singularityhub/sregistry
```

Remember that the `rse.ini` needs to be in the present working directory, or specified
with `--config_file`. You can also list a particular parser:

```bash
$ rse ls github
DATABASE: filesystem
INFO:rse.main:Database: filesystem
1  github/singularityhub/sregistry
```

<a id="clear">
## Clear

If you want to delete a software entry, just use clear with it's unique id:

```bash
$ rse clear github.com/singularityhub/sregistry
INFO:rse.main:Database: filesystem
This will delete software github.com/singularityhub/sregistry, are you sure? [n]|y: y
INFO:rse.main.database.filesystem:github.com/singularityhub/sregistry has been removed.
```

You can also remove an entire parser:

```bash
$ rse clear github
INFO:rse.main:Database: filesystem
This will delete all github software in the database, are you sure? [n]|y: y
```

or all software repositories in the database:

```bash
$ rse clear
DATABASE: filesystem
This will delete all software in the database, are you sure? [n]|y: y
INFO:rse.main.database.filesystem:Removing /home/vanessa/Desktop/Code/rseng/software/database/github
```

Each time you'll be asked for a confirmation first, in case the command was 
run in error.



<a id="search">
## Search

We can easily search across our software repos with search. For a filesystem
database, this means only the filenames.

```bash
$ rse search term
INFO:rse.main:Database: filesystem
INFO:rse.main:No results matching term
```

Here is an example with results:
```bash
$ rse search singularity
INFO:rse.main:Database: filesystem
1  github/singularityhub/sregistry
```

<a id="shell">
## Shell

The shell is a quick way to open up an interactive environment with an encyclopedia
client. For example, let's say we are sitting at the root of a database, such as the
repository rseng/software:

```bash
git clone git@github.com:rseng/software.git
cd software
```

This means that we have an rse.ini file, and can then start a shell to interact
with the software there:

```
$ rse shell
INFO:rse.main:Database: sqlite
Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

client                                                                                                              
Out[1]: <rse.main.Encyclopedia at 0x7f2135346690>
```

From that point on, you'd be interacting with the Encyclopedia client.

<a id="start">
## Start

The rse start command will open a web interface with an interactive table
for your tasks. 

```bash
$ rse start
```

You can run it in debug mode:

```bash
$ rse start --debug
```

or further customize the port or hostname

```bash
$ rse start --port 8000 --host 0.0.0.0
```

For each, you can specify a particular action (e.g., delete or re-run)
or click on it for further details.  See the [dashboard]({{ site.baseurl }}/getting-started/dashboard/) 
documentation page for more details.
