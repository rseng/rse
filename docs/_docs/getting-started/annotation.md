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

## Interface Annotation

When you start the Research Software Encyclopedia interface with `rse start`,
akin to doing on the command line, you might want to export your `RSE_CONFIG_FILE`

```bash
export RSE_CONFIG_FILE=/path/to/rseng/software
```

and then start the interface!

```bash
$ rse start
```

then you can select an "annotate" button at the top in order to annotate taxonomy
items or criteria:

![../img/annotate/annotate-button.png](../img/annotate/annotate-button.png)

You can then select to annotate either criteria or taxonomy items. You are
required to put your GitHub username at the top, as the repository
will be updated as you go, and you'll want to have your results saved
with the correct username (new or updated results that don't match your
username will not be accepted).

![../img/annotate/annotate.png](../img/annotate/annotate.png)

For each item you haven't annotated yet, you'll be presented with the current
questions in the interface. You can answer as many as you like! Here is
the view for criteria:

![../img/annotate/annotate-repo.png](../img/annotate/annotate-repo.png)

