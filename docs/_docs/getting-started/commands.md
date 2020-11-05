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
 - [Scrape](#scrape): automated update of new software repositories from a remote resource
 - [Update](#update): update metadata for a single repository or all repositories
 - [Label](#label) a software repository with custom metadata
 - [List](#list) all software or software specific to a parser
 - [Export](#export) list of software, or static interface

 - [Clear](#clear) a software repository, all under a parser, or the entire database.
 - [Search](#search) across your software to find a particular one.
 - [Summary](#summary) to summarize your research software database.
 - [Analyze](#analyze) a specific software repository, indicating a consensus/summary about criteria and taxonomy.
 - [Shell](#shell) into a Python shell to interact with an encyclopedia client.
 - [Start](#start) an interactive dashboard to see software and annotate crtieria and taxonomy membership.
 - [Topics](#topics) list topics (tags) associated with a repository

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

And of course you can add urls for other version control systems that are supported.

```bash
$ rse add gitlab.com/singularityhub/gitlab-ci
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

<a id="scrape">
## Scrape

Adding a repository here and there is logical, but it would be very arduous
to need to consistently look for and add new software repositories. Toward
this goal, the research software encyclopedia has a `scrape` command
that will allow you to programaticaly discover new repos from some
external resource. For example, if we wanted to query the [Journal of Open Source Software](https://joss.theoj.org/)

```bash
$ rse scrape joss
```

If you don't provide a query term, the latest set will be returned. If you do
provide a term,

```bash
$ rse scrape joss docker
```

The term will be searched for instead. You can also do a dry run to see the 
repos found, but not add them to the software repository:

```bash
$ rse scrape --dry-run joss
```

For more detailed scraping, it's recommended
to interact with a scraper from within Python. See the [scrapers](../scrapers) getting
started pages to do this.

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

By default, repos that are not present will be skipped over. If you want
to rewrite existing metadata (for example, if you change the structure of the data)
you can add the `--rewrite` flag:

```bash
$ rse update --file repos.txt --rewrite
```

This works for single repository updates as well.

<a id="label">
## Label

Let's say that we know a DOI (digital object identifier) for a repository,
and we want to label it. We can do that as follows:

```bash
$ rse label github/singularityhub/sregistry doi 10.5281/zenodo.1012531
INFO:rse.main:Database: sqlite
INFO:rse.main:github/singularityhub/sregistry has been updated.
```

The above command would say "Add the metadata value for "doi" to the Github
repository for Singularity Registry server. You would then see the value in the
metadata:

```bash
$ rse get
INFO:rse.main:Database: sqlite
{
    "parser": "github",
    "uid": "github/singularityhub/sregistry",
    "data": {
        "timestamp": "2020-06-19 16:26:07.115675",
...
        "subscribers_count": 10,
        "doi": "10.5281/zenodo.1012531"
    }
}
```

If you try to add a value that 
already exists, you'll get a warning and be asked to use `--force`.

```bash
INFO:rse.main:Database: sqlite
doi is already defined for github/singularityhub/sregistry. Use --force to overwrite.
```

Although it's less likely for someone
to do this on the command line, the function is used by scrapers when a link
is found between a software respository and some external DOI.

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

<a id="export">
## Export

If you want to export a flat listing of repos, you can do so like:

```bash
$ rse export repos.txt
```

The default filename is repos.txt, so you could also leave this out:

```bash
$ rse export
```

The `--type` is a variable that can be changed to indicate an export of a static
interface, which will start the web server, and then query endpoints to export
static files to some folder of interest. You're also required to indicate a path.

```bash
$ rse export --type static-web docs/
```

If the folder already exists and you want to over-write, it's suggested to remove
it first and then run, but if you want to overwrite without removal, just add `--force`

```bash
$ rse export --type static-web --force docs/
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

For a filesystem database, you can also search across taxonomy and/or criteria items:

```bash
$ rse search --taxonomy package
RSE-taxonomy-package-management
1  github/easybuilders/easybuild
2  github/spack/spack

$ rse search --criteria research
RSE-research-intention
1  github/AA-ALERT/AstroData
2  github/fair-software/howfairis
3  github/BrianAronson/birankr
4  github/3D-e-Chem/knime-sstea
5  github/davidebolo1993/TRiCoLOR
6  github/AA-ALERT/AMBER
7  gitlab/davidtourigny/dynamic-fba
8  github/Sulstice/cocktail-shaker
9  github/spack/spack
10 github/snakemake/snakemake
11 github/potree/PotreeConverter
12 github/Effective-Quadratures/Effective-Quadratures
13 github/3D-e-Chem/knime-pharmacophore
14 github/sunpy/sunpy
15 github/AA-ALERT/frbcatdb
16 github/AA-ALERT/frbcat-web
17 github/Parsl/parsl
18 github/JuliaOpt/JuMP.jl
19 github/AA-ALERT/Dedispersion
20 github/scikit-image/scikit-image
21 github/3D-e-Chem/sygma
22 github/nextflow-io/nextflow
23 gitlab/LouisLab/PiVR
24 github/3D-e-Chem/knime-gpcrdb
25 gitlab/cosmograil/PyCS3
26 github/sjvrijn/mf2
27 github/KVSlab/turtleFSI
28 github/ropensci/chirps
29 gitlab/ampere2/metalwalls
```

The searches are independent, meaning that you might see the same repository in two
results listings if it has more than one match for a given taxonomy or criteria item.
The same is true for adding a search term at the onset:

```python
$ rse search singularity --taxonomy package
singularity
1  github/hpcng/singularity
2  github/singularityhub/singularity-compose
3  github/singularityhub/sregistry
4  github/eWaterCycle/setup-singularity

RSE-taxonomy-package-management
1  github/spack/spack
2  github/easybuilders/easybuild
```

<a id="summary">
## Summary

You might want a quick summary of the annotations, whether taxonomy or criteria,
or number of unique users that have annotated your database. The `summary` command
can help you here.

```bash
$ rse summary
INFO:rse.main:Database: filesystem
{
    "repos": 86,
    "taxonomy-count": 17,
    "criteria-count": 6,
    "users": {
        "vsoch": {
            "criteria-annotations": 2,
            "taxonomy-annotations": 0
        }
    },
    "taxonomy": {
        "github/vsoch/gridtest": {
            "RSE-taxonomy-numerical-libraries": 1
        },
        "github/singularityhub/sregistry": {
            "RSE-taxonomy-databases": 1,
            "RSE-taxonomy-application-programming-interfaces": 1
        }
    },
    "criteria": {
        "github/singularityhub/sregistry": {
            "yes": 1,
            "no": 0
        },
        "github/singularityhub/singularity-compose": {
            "yes": 0,
            "no": 1
        }
    },
    "users-count": 1
}
```

You can also ask to show just metrics associated with taxonomy, criteria, or users:

```bash
$ rse summary --type criteria
INFO:rse.main:Database: filesystem
{
    "criteria": {
        "github/singularityhub/sregistry": {
            "yes": 1,
            "no": 0
        },
        "github/singularityhub/singularity-compose": {
            "yes": 0,
            "no": 1
        }
    },
    "criteria-count": 6,
    "repos": 86
}
```
```bash
$ rse summary --type taxonomy
INFO:rse.main:Database: filesystem
{
    "taxonomy": {
        "github/vsoch/gridtest": {
            "RSE-taxonomy-numerical-libraries": 1
        },
        "github/singularityhub/sregistry": {
            "RSE-taxonomy-databases": 1,
            "RSE-taxonomy-application-programming-interfaces": 1
        }
    },
    "taxonomy-count": 17,
    "repos": 86
}
```
```bash
$ rse summary --type users
INFO:rse.main:Database: filesystem
{
    "users-count": 1,
    "users": {
        "vsoch": {
            "criteria-annotations": 2,
            "taxonomy-annotations": 0
        }
    },
    "repos": 86
}
```

or ask to filter down to one repository:

```bash
$ rse summary github/singularityhub/sregistry
INFO:rse.main:Database: filesystem
{
    "repo": "github/singularityhub/sregistry",
    "taxonomy-count": 17,
    "criteria-count": 6,
    "users": {
        "vsoch": {
            "criteria-annotations": 1,
            "taxonomy-annotations": 0
        }
    },
    "taxonomy": {
        "github/singularityhub/sregistry": {
            "RSE-taxonomy-databases": 1,
            "RSE-taxonomy-application-programming-interfaces": 1
        }
    },
    "criteria": {
        "github/singularityhub/sregistry": {
            "yes": 1,
            "no": 0
        }
    },
    "users-count": 1
}
```

<a id="analyze">
## Analyze

Analyze can provide metrics (or calculations) specific to a single repository, or
across all repositories. We will start with the single repository example first.
Let's say that we want to analyze the repository `github.com/singularityhub/sregistry`.
For criteria, by default it will give you a "final answer" of yes/no depending on the majority,
or indicate a tie otherwise. For taxonomy items, it will list all categories with > 1 vote.

```bash
$ rse analyze github/singularityhub/sregistry
INFO:rse.main:Database: filesystem
Summary for github/singularityhub/sregistry

Criteria
1  yes	Would taking away the software be a detriment to research?
2  no	Is the software intended for a particular domain?
3  no	Was the software created with intention to solve a research question?
4  no	Is the software intended for research?
5  yes	Has the software been used by researchers?
6  yes	Has the software been cited?

Taxonomy
1  1	Databases
2  1	Application Programming Interfaces
```

The above shows us that the majority (>50%) said that taking away the software would
be a detriment to research, and that it's been used and cited by researchers. The taxonomy
categories that were voted for (greater than 1 user) include Databases and application programming
interfaces. You can change these thresholds easily:

```bash
$ rse analyze github/singularityhub/sregistry --cthresh 0.6 --tthresh 2
```

For the above, we wouldn't have any taxonomy results because there are none with more
than two votes. If you want to do a bulk analysis for all repositories, you
are required to use the internal client:

```python
from rse.main import Encyclopedia
client = Encyclopedia()
```

The client analyze_bulk function takes the same arguments, but returns a large json
structure with all repos that have annotations for criteria or taxonomy categories.

```python
client.analyze_bulk()
[{'repo': 'github/vsoch/gridtest',
  'criteria': {},
  'taxonomy': {'RSE-taxonomy-numerical-libraries': 1}},
 {'repo': 'github/singularityhub/sregistry',
  'criteria': {'RSE-absence': 'yes',
   'RSE-domain-intention': 'no',
   'RSE-question-intention': 'no',
   'RSE-research-intention': 'no',
   'RSE-usage': 'yes',
   'RSE-citation': 'yes'},
  'taxonomy': {'RSE-taxonomy-databases': 1,
   'RSE-taxonomy-application-programming-interfaces': 1}},
 {'repo': 'github/singularityhub/singularity-compose',
  'criteria': {'RSE-absence': 'yes',
   'RSE-domain-intention': 'no',
   'RSE-question-intention': 'no',
   'RSE-research-intention': 'no',
   'RSE-usage': 'yes',
   'RSE-citation': 'no'},
  'taxonomy': {}}]
```

If you want to include empty repos (without votes) set `include_empty` to True.


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

<a id="topics">

## Topics

As of version 0.0.29, the Research Software Encyclopedia has support for topics,
primarily for the GitHub parser. If you have an older verison you can update your
metadata with:

```bash
rse update github/<usename>/<repo>
```

or export all names to file, and bulk update

```bash
rse export repos.txt
rse update --file repos.txt
```

Then you can ask to list topics, for example filtered by a pattern:

```bash
$ rse topics --pattern meta
INFO:rse.main:Database: filesystem
metadata-extraction
metadata
```

If you want to see topics for a single repository, they are part of the standard
metadata returned by get:

```bash
$ rse get github/<usename>/<repo>
```

If you want to list all unique topics:

```bash
$ rse topics
INFO:rse.main:Database: filesystem
cli
client
cloud-native
container
container-friends
container-orchestration
containers
cosmology
date
date-parser
datetime
docker
entity-extraction
hdf5
hpc
html-parsing
information-extraction
linux
management
metadata
metadata-extraction
natural-language-processing
nlp
parallel
particle
portability
portable
registry
reproducible
reproducible-science
rootless-containers
science
singularity
singularity-compose
singularity-container
singularity-containers
singularity-python
singularityhub
web-scraping
webscraping
```

Finally, you can search for one or more topics, and find repositories that are labeled 
as such:

```bash
$ rse topics --search science
INFO:rse.main:Database: filesystem
github/JuliaLang/julia
github/MD-Studio/MDStudio
github/MDAnalysis/mdanalysis
github/SCM-NV/qmflows
github/SCM-NV/qmflows-namd
github/astropy/astropy
github/hpcng/singularity
github/recipy/recipy
```
