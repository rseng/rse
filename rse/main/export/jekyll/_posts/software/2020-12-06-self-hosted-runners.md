---
layout: post
title: "self-hosted-runners"
date: 2020-12-06
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/ci-for-science/self-hosted-runners/annotate-criteria/index.html
annotate_taxonomy: https://rseng.github.io/software/repository/github/ci-for-science/self-hosted-runners/annotate-taxonomy/
categories:
- Software
---

Did you know that you can use [self hosted runners](https://docs.github.com/en/free-pro-team@latest/actions/hosting-your-own-runners/about-self-hosted-runners) for GitHub actions? For this non-traditional research software showcase, we want to introduce you to [ci-for-science/self-hosted-runners](https://github.com/ci-for-science/self-hosted-runners/), a repository of recipes to help you get started with your own self hosted runners!

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/self-hosted-runners.png]({{ site.baseurl }}/assets/img/posts/showcase/self-hosted-runners.png)

<br>

Are you already familiar with self-hosted-runners? We encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is nodepy?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I get started?](#getting-started)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)

<a id="what-is">
## What is a self hosted runner?

You can think of a runner as a server (somewhere, either one that you control or in the cloud) that you can use to run your tests, container builds, and other kinds of continuous integration. In the case of GitHub actions, the service provides documentation for [self hosted runners](https://docs.github.com/en/free-pro-team@latest/actions/hosting-your-own-runners/about-self-hosted-runners) that give you a high level overview of getting started.

#### Why is it useful?

However, mapping this documentation to real world examples, especially if you are low on bandwidth, can take a lot of time. This is the reason to have repositories like [ci-for-science/self-hosted-runners](https://github.com/ci-for-science/self-hosted-runners/).
The `self-hosted-runners` repository can quickly give you complete instructions for multiple
different kinds of configurations. Do you want to use a container technology on your local machine? or maybe a cloud that you control? This respository can get you started!

Resources like this repository may not be considered traditional research software, but we can't deny the value to the research ecosystem to have them. For this reason, the Research Software Encyclopedia aims to also share them proudly.

<a id="cite">
## How do I cite it?

The repository [DOI](https://doi.org/10.5281/zenodo.3904265) comes by way of Zenodo:

```
@software{zapata_felipe_2020_3904800,
  author       = {Zapata, Felipe and
                  Diblen, Faruk and
                  Verhoeven, Stefan and
                  Spaaks, Jurriaan H. and
                  Spreeuw, Hanno},
  title        = {Self-hosted runners},
  month        = jun,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.2.0},
  doi          = {10.5281/zenodo.3904800},
  url          = {https://doi.org/10.5281/zenodo.3904800}
}
```

<a id="getting-started">
## How do I get started?
 
 - [GitHub Documentation](https://github.com/ci-for-research/self-hosted-runners)
 - [research-software.nl](https://research-software.nl/software/self-hosted-runners) has the original posting.

And if you are a developer, it would be fun to contribute new recipes for runners that are not added yet.


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
