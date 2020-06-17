---
title: Annotation
category: Tutorials
permalink: /tutorials/annotation/index.html
order: 2
---

The most likely task you'll want to do is provide your input to annotate
the existing research software database at [github.com/rseng/software](https://github.com/rseng/software).
This tutorial will walk you through how to do that, both using the command line
and a web interface (under development).


## Clone the repository

Whether or not you use the interface or command line, you need to start
with a set of software to annotate! You might start your own software repository with `rse init`, but likey you
want to annotate one that already exists. Let's clone it now.

```bash
$ git clone https://github.com/rseng/software
cd software
```

The default database in the `rse.ini` is the filesystem, which means the research
software encyclopedia knows how to annotate it. If you intend to contribute your
annotations back to respository (we hope that you do!) then it might be a good idea
to checkout a new branch:

```bash
git checkout -b annotation/user-vsoch
```

### Environment

To annotate criteria, if you aren't sitting in the root of the repository, you
might want to export your `RSE_CONFIG_FILE` to be where the repository is. For example:

```bash
$ export RSE_CONFIG_FILE=/path/to/rseng/software/rse.ini
```

## Command Line Annotation

To annotate from the command line, you can choose `rse annotate` and target
either criteria or the taxonomy.

```bash
$ rse annotate taxonomy
$ rse annotate criteria
```

Since we use GitHub usernames to determine who has annotated what, if your
GitHub username is not available via:

```bash
git config user.name
```
then you'll need to provide that as an argument:

```bash
$ rse annotate taxonomy -u vsoch
$ rse annotate criteria -u vsoch
```

### Annotate All Unseen Software Repositories

By default, running an annotation session will annotate all software that your
GitHub username has not seen.

```bash
$ rse annotate taxonomy
$ rse annotate criteria
```

If you want to re-annotate repositories that you've seen, then specify that:

```bash
$ rse annotate taxonomy --all
$ rse annotate criteria --all
```

For each annotation, the repository is saved after you answer all questions for it.
This means if you press Control+C during any time, the repositories you've finished
annotation for will be saved.

### Annotate Single Repository

It might be preferable for you to annotate a specific repository. For each
of the below, you are provided a url to explore further along with a description,
if needed.

**criteria**

```bash
$ rse annotate criteria -r github/singularityhub/sregistry
INFO:rse.main:Database: filesystem

https://github.com/singularityhub/sregistry [server for storage and management of singularity images]:
Would taking away the software be a detriment to research? [n]|y: y
Has the software been cited? [n]|y: y
Is the software intended for a particular domain? [n]|y: n
Was the software created with intention to solve a research question? [n]|y: n
Is the software intended for research? [n]|y: n
Has the software been used by researchers? [n]|y: y
```

After the annotation session, you can use `git status` to see that the criteria you answered
for, and the repositories that you answered questions for, will have changed files:

```bash
$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	database/github/singularityhub/sregistry/criteria-RSE-absence.tsv
	database/github/singularityhub/sregistry/criteria-RSE-citation.tsv
	database/github/singularityhub/sregistry/criteria-RSE-domain-intention.tsv
	database/github/singularityhub/sregistry/criteria-RSE-question-intention.tsv
	database/github/singularityhub/sregistry/criteria-RSE-research-intention.tsv
	database/github/singularityhub/sregistry/criteria-RSE-usage.tsv
```

In the case of this example, we had not yet seen the repositories, so they are new files.
We would then add the files, and push to our branch, and open a pull request to the
repository. Here is an asciinema that shows how annotation looks:

<script id="asciicast-340558" data-speed="2" src="https://asciinema.org/a/340558.js" async></script>


**taxonomy**

You might also want to annotate repositories for the taxonomy. This means that you will
be shown a repository, a list of categories, and asked to place the software in one or
more categories (up to you!)

```bash
$ rse annotate taxonomy -r github/singularityhub/sregistry

https://github.com/singularityhub/sregistry [server for storage and management of singularity images]:
How would you categorize this software? [enter one or more numbers]
[0] Domain-specific analysis software (SPM, fsl, afni for neuroscience)
[1] Application Programming Interfaces
[2] Communication tools or platforms (email, slack, etc.)
[3] Data collection (web-based experiments or portals)
[4] Databases
[5] Domain-specific hardware (software for physics to control lab equipment)
[6] Frameworks (to generate documentation, content management systems)
[7] Interactive development environments for research (Matlab, Jupyter)
[8] Numerical libraries (includes optimization, statistics, simulation, e.g., numpy)
[9] Operating systems
[10] Domain-specific optimized software (neuroscience software optimized for GPU)
[11] Personal scheduling and task management
[12] Provenance and metadata collection tools
[13] Text editors and integrated development environments
[14] Version control
[15] Visualization (interfaces to interact with, understand, and see data, plotting tools)
[16] Workflow managers
Please enter one or more numbers, separated by spaces
Please enter your choice [0:16] : 1 4
```

And after your session, you can see that the taxonomy file for the repository has
been added or updated.

```bash
$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	database/github/singularityhub/sregistry/taxonomy.tsv
```

Here is a quick view of what this looks like interactively.

<script id="asciicast-340590" data-speed="2" src="https://asciinema.org/a/340590.js" async></script>
