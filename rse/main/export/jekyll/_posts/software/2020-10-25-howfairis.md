---
layout: post
title: "howfairis"
date: 2020-10-25 08:30:46
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/fair-software/howfairis/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/fair-software/howfairis/annotate-taxonomy/
categories:
- Software
---

Have you heard of the [Fair principes](https://www.go-fair.org/fair-principles/)? 
Or perhaps you've generally thought about what makes software:

- Findable
- Accessible
- Interoperable
- Reusable

This week we highlight an atypical piece of research software, <a href="https://github.com/fair-software/howfairis" target="_blank">fair-software/howfairis</a> that helps to make some of these abstract ideas more concrete, meaning giving you actionable feedback about the status of your GitHub repository. Why is it atypical? Because likely some folks would
not consider this research software. But perhaps others would, because it's a meta library that has promise to be used
in a research context to better understand our software.

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/howfairis.png]({{ site.baseurl }}/assets/img/posts/showcase/howfairis.png)

<br>

Do you have an opinion? We encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is howfairis?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I get started?](#getting-started)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is Howfairis?

There are several attributes of software that are important for reproducibility.
However, for the most part unless you do a manual evaluation of some software, you
can't easily evaluate some repository for these criteria. The goal of Howfairis is to
make this evaluation possible. You can install the software:

```bash
pip install howfairis
```

And then immediately evaluate a repository for the four principles.

```bash
$ howfairis https://github.com/singularityhub/sregistry
Checking compliance with fair-software.eu...
url: https://github.com/singularityhub/sregistry
(1/5) repository
      ✓ has_open_repository
(2/5) license
      ✓ has_license
(3/5) registry
      × has_ascl_badge
      × has_bintray_badge
      × has_conda_badge
      × has_cran_badge
      × has_crates_badge
      × has_maven_badge
      × has_npm_badge
      × has_pypi_badge
      × has_rsd_badge
      × is_on_github_marketplace
(4/5) citation
      × has_citation_file
      × has_citationcff_file
      × has_codemeta_file
      ✓ has_zenodo_badge
      × has_zenodo_metadata_file
(5/5) checklist
      × has_core_infrastructures_badge
      × has_sonarcloud_badge

Calculated compliance: ● ● ○ ● ○

It seems you have not yet added the fair-software.eu badge to
your README.md. You can do so by pasting the following snippet:

[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F%20%20%E2%97%8B-orange)](https://fair-software.eu)
```

How neat! And then if you own the software, you can also add the badge to your repository.
For example, I did it for [Singularity Registry Server](https://github.com/singularityhub/sregistry):

![{{ site.baseurl }}/assets/img/posts/showcase/howfairis-badge.png]({{ site.baseurl }}/assets/img/posts/showcase/howfairis-badge.png)


#### Why is it useful?

I would actually suspect this to be useful from a research standpoint. Sure, it's fun 
to evaluate our own software and add badges, but what if we could do this programatically
for a bunch of repositories we want to study? I took a look at the code base, and wrote a little
snippet to show how to programatically test a repository.

```python
from howfairis.cli import Repo, Config, Checker, check_badge

# I suspect you could just define a path to a cloned repository here
repo = Repo(url="https://github.com/singularityhub/sregistry", branch="master", path=None)

# Use defaults
config = Config(repo)
checker = Checker(config)
checker.check_five_recommendations()
```

You then have the README from the repository

```python
checker.readme
# <howfairis.Readme.Readme at 0x7ffbbb8708e0>
checker.readme.text
```

Along with the compliance 

```python
checker.compliance
<howfairis.Compliance.Compliance at 0x7ffbbb8607c0>
```

which you can parse for different attributes.

```python
checker.compliance.checklist
False

checker.compliance.citation
True

checker.compliance.license
True

checker.compliance.registry
False
```

And you can also run a function to check for a badge.

```python
check_badge(compliance=checker.compliance, readme=checker.readme)
Calculated compliance: ● ● ○ ● ○

Expected badge is equal to the actual badge. It's all good.
```

The function system exits because it's intended to be run from a client, which
might not be ideal design if you want to do this programatically.

<a id="cite">
## How do I cite it?

The package has a <a href="https://zenodo.org/record/4036809#.X5XQJK5ME5k" target="_blank">record on Zenodo</a> that you can use:

```
@software{spaaks_jurriaan_h_2020_4036809,
  author       = {Spaaks, Jurriaan H. and
                  Kuzak, Mateusz and
                  Martinez-Ortiz, Carlos and
                  van Werkhoven, Ben and
                  Etuk, Edidiong and
                  Saladi, Shyam and
                  Holding, Andrew},
  title        = {howfairis},
  month        = sep,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.11.0},
  doi          = {10.5281/zenodo.4036809},
  url          = {https://doi.org/10.5281/zenodo.4036809}
}
```

<a id="getting-started">
## How do I get started?
 
 - [README Documentation](https://github.com/fair-software/howfairis#howfairis) is always a good place to start.

<a id="contribute">
## How do I contribute to the software survey?

<ul>
  <li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
  <li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

or read more about annotation [here]({{ site.baseurl }}/tutorials/annotate-your-software). You can clone the software repository to do
bulk annotation, or annotation any repository in the <a href="https://rseng.github.io/software/" target="_blank">software database</a>,
We want annotation to be fun, straight-forward, and easy, so we will be showcasing one repository to annotate per week.
If you'd like to request annotation of a particular repository (or addition to the software database)
please don't hesitate to [open an issue](https://github.com/rseng/software/issues) or even a pull request.

<a id="learn-more">
## Where can I learn more?

You might find these other resources useful:

 - [The Research Software Database](https://github.com/rseng/software) on GitHub
 - [RSEpedia Documentation](https://rseng.github.io/rse)
 - [Google Docs Manuscript](https://docs.google.com/document/d/1wDb0udH9OrFWrMBsAVb8RrUMCKKRHoyEep7yveJ1d0k/edit) you are invited to contribute to.
 - [Annotation Documentation for RSEpedia](https://rseng.github.io/rse/tutorials/annotation/)
 - [Annotation Tutorial in RSEng docs](https://rseng.github.io/rse/tutorials/annotation/)

For any resource, you are encouraged to give feedback and contribute!
