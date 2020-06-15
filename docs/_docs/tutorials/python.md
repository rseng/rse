---
title: Python
category: Tutorials
permalink: /tutorials/python/index.html
order: 3
---

You might want to interact with a software database via Python. 

> Why would I want to do that?

You might want to contribute repositories to a database, or just use it for your
own analysis. In this walkthrough, we will clone the the [github.com/rseng/software](https://github.com/rseng/software)
database, checkout a new branch, and then make changes that we would intend
to do a pull request to contribute back.

## Get the Database

While you could start from scratch and create your own database with `rse init`
and then `rse add`, it's more likely you'll want to start with an already
existing base. Let's do that by cloning:

```bash
git clone https://github.com/rseng/software
cd software
```

You will notice an `rse.ini` file that has a basic configuration for the filesystem.
While other formats are supported, because we want to keep this database in version
control, a filesystem format is optimal. Once we have our repository cloned,
we can start a shell to interact with it:

```bash
$ rse shell
...
client                                                                                                              
Out[1]: <rse.main.Encyclopedia at 0x7fb543b25590>
```

And remember that you can always export the full path to an rse.ini config file,
in the case that you want to be able to run `rse shell` from anywhere:

```bash
export RSE_CONFIG_FILE=/home/vanessa/Desktop/Code/rseng/software/rse.ini
```

## Commands

All of the commands that are available on the command line (and a few more)! are available to you.

 - [Exists](#exists): determine if a particular repository exists in your local repository
 - [Add](#add): add a new software repository to your database
 - [Get](#get): retrieve current metadata for a piece of software, or all software
 - [Update](#update): update metadata for a single repository or all repositories
 - [List](#list) all software or software specific to a parser

 - [Remote](#remote): query the rseng/software remote database
 - [Clear](#clear) a software repository, all under a parser, or the entire database.
 - [Search](#search) across your software to find a particular one.

 - [Criteria](#criteria): list criteria from the rseng criteria and taxonomy API

<a id="exists">
## Exists

Does a particular software repository exists in your database?

```bash
$ client.exists("github.com/singularityhub/sregistry")
True

$ client.exists("github.com/singularityhub/pancakes")
False
```

<a id="add">
## Add

Let's say that we tested if our software of interest existed in the repository,
and then we found that it did not, and want to add it. We can use `rse add`
to do this.

```bash
$ client.add("github.com/sci-f/scif-go")
INFO:rse.main.database.relational:github/sci-f/scif-go was added to the the database.
```

Ah! But don't forget that you need to export your `RSE_GITHUB_TOKEN`.
If the entry already exists, you will be told that!

```bash
$ client.add("github.com/sci-f/scif-go")
ERROR:rse.main:github.com/sci-f/scif-go already exists in the database.
```

And if the entry doesn't exist on the remote (e.g., GitHub) you'll see:

```bash
$ client.add("github.com/singularityhub/pancakes")
ERROR:rse.main.parsers.github:Cannot find repository singularityhub/pancakes.
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
$ client.bulk_add("repos.txt")
```

By default, repos that are already added will be skipped over.


<a id="get">
## Get 

A get will retrieve a known identifier. Unlike exists, if it doesn't exist, it will
parse and retrieve it for you.

```bash
$ repo = client.get("github.com/singularityhub/sregistry")
# <SoftwareRepository 'github/singularityhub/sregistry'>
```

You can then inspect, export, or otherwise interact with the repository instance.

```bash
repo.data
repo.uid
repo.export()
repo.load()
repo.parser
repo.summary()
repo.timestamp
```

If you run get without an argument, it will retrieve the last modified entry
for you:

```bash
$ client.get()
# <SoftwareRepository 'github/sci-f/scif-go'>
```

<a id="update">
## Update

Updating an entry coincides with retriving updated metadata. You can do this
for an existing software repository:

```python
> client.update("github.com/singularityhub/sregistry")
INFO:rse.main:github/singularityhub/sregistry has been updated.
# <SoftwareRepository 'github/singularityhub/sregistry'>
```

And of course you cannot update an entry that doesn't exist.

```bash
$ client.update("github.com/singularityhub/noodles")
ERROR:rse.main:github.com/singularityhub/noodles does not exist.
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
$ client.bulk_update("repos.txt")
```

By default, repos that are not present will be skipped over.


<a id="list">
## List

We can easily list repos with list.

```python
> client.list()
[['github/singularityhub/sregistry'],
 ['github/scikit-learn/scikit-learn'],
 ['github/tensorflow/tensorflow'],
 ['github/mlpack/mlpack'],
 ['github/sunpy/sunpy'],
 ['github/stan-dev/stan'],
...
 ['github/mathjax/MathJax'],
 ['github/optuna/optuna'],
 ['github/PyTables/PyTables'],
 ['github/nteract/nteract'],
 ['github/yt-project/yt'],
 ['github/ropensci/rtweet'],
 ['github/sci-f/scif-go']]
```

You can also list a particular parser:

```python
> client.list("github")
```

<a id="clear">
## Clear

If you want to delete a software entry, just use clear with it's unique id:

```python
> client.clear("github.com/singularityhub/sregistry")
This will delete software github.com/singularityhub/sregistry, are you sure? [n]|y: y
```

If you don't want the prompt, add `noprompt=True`

```python
> client.clear("github.com/singularityhub/sregistry", noprompt=True)
```

You can also remove an entire parser:

```python
> client.clear("github")
This will delete all github software in the database, are you sure? [n]|y: y
```

or all software repositories in the database:

```python
> client.clear()
This will delete all software in the database, are you sure? [n]|y: y
```

Unless you set `noprompt` to True, each time you'll be asked for a confirmation first, in case the command was 
run in error.

<a id="search">
## Search

We can easily search across our software repos with search. For a filesystem
database, this means only the filenames.

```python
> client.search("singularity")
[['github/singularityhub/sregistry', 'github', '2020-06-09 17:59:41'],
 ['github/hpcng/singularity', 'github', '2020-06-09 19:44:04']]
```

Depending on your database backend, you might retrieve more metadata (the above is
for the sqlite backend).

<a id="criteria">
## Criteria

The criteria that we use to populate the client is the present version available
from [https://rseng.github.io/rseng]. If you need an earlier verison, you can
interact with the rseng library directly. To do this with the client here,
you can simply list criteria:

```python
> client.list_criteria()
[{'uid': 'RSE-absence',
  'name': 'Would taking away the software be a detriment to research?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'},
 {'uid': 'RSE-citation',
  'name': 'Has the software been cited?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'},
 {'uid': 'RSE-domain-intention',
  'name': 'Is the software intended for a particular domain?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'},
 {'uid': 'RSE-question-intention',
  'name': 'Was the software created with intention to solve a research question?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'},
 {'uid': 'RSE-research-intention',
  'name': 'Is the software intended for research?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'},
 {'uid': 'RSE-usage',
  'name': 'Has the software been used by researchers?',
  'options': ['yes', 'no'],
  'date': '2020-06-13 15:04:25 +0000'}]
```


<a id="taxonomy">
## Taxonomy

You can also list a flattened version of the taxonomy from
from [https://rseng.github.io/rseng]. 

```python
> client.list_taxonomy()
[{'uid': 'RSE-taxonomy-analysis',
  'name': 'Domain-specific analysis software',
  'example': 'SPM, fsl, afni for neuroscience',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-application-programming-interfaces',
  'name': 'Application Programming Interfaces',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-communication-tools',
  'name': 'Communication tools or platforms',
  'example': 'email, slack, etc.',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-data-collection',
  'name': 'Data collection',
  'example': 'web-based experiments or portals',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-databases',
  'name': 'Databases',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-domain-hardware',
  'name': 'Domain-specific hardware',
  'example': 'software for physics to control lab equipment',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-frameworks',
  'name': 'Frameworks',
  'example': 'to generate documentation, content management systems',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-ide-research',
  'name': 'Interactive development environments for research',
  'example': 'Matlab, Jupyter',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-numerical libraries',
  'name': 'Numerical libraries',
  'example': 'includes optimization, statistics, simulation, e.g., numpy',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-operating-systems',
  'name': 'Operating systems',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-optimized',
  'name': 'Domain-specific optimized software',
  'example': 'neuroscience software optimized for GPU',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-personal-scheduling-task-management',
  'name': 'Personal scheduling and task management',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-provenance-metadata-tools',
  'name': 'Provenance and metadata collection tools',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-text-editors-ides',
  'name': 'Text editors and integrated development environments',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-version-control',
  'name': 'Version control',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-visualization',
  'name': 'Visualization',
  'example': 'interfaces to interact with, understand, and see data, plotting tools',
  'date': '2020-06-13 14:48:53 +0000'},
 {'uid': 'RSE-taxonomy-workflow-managers',
  'name': 'Workflow managers',
  'date': '2020-06-13 14:48:53 +0000'}]
```
