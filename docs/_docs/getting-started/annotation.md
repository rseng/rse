---
title: Annotation
category: Getting Started
permalink: /getting-started/annotation/index.html
order: 9
---

The research software encyclopedia makes it very easy to annotate software
repositories with criteria or taxonomy items. The pages here show
basic interaction to annotate, and it's recommended to read the [annotation tutorial]({{ site.baseurl }}/tutorials/annotation/) for a complete walkthrough of cloning the https://github.com/rseng/software repository
and submitting your annotations to add to the database.

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

By default, running an annotation session will annotate all software that your
GitHub username has not seen.
However, if you want to re-annotate repositories that you've seen, then specify that:

```bash
$ rse annotate taxonomy --all
$ rse annotate criteria --all
```

For each annotation, the repository is saved after you answer all questions for it.
This means if you press Control+C during any time, the repositories you've finished
annotation for will be saved. If you want to annotate a specific repository, you
can specify it:

```bash
$ rse annotate criteria -r github/singularityhub/sregistry
$ rse annotate taxonomy -r github/singularityhub/sregistry
```
