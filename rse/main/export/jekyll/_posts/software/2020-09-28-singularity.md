---
layout: post
title: "Singularity"
date: 2020-09-28 08:30:46
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/hpcng/singularity/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/hpcng/singularity/annotate-taxonomy/
categories:
- Software
---

Do you remember the reproducibility crisis? It's a term so well-coined that it's on <a href="https://en.wikipedia.org/wiki/Replication_crisis" target="_blank">Wikipedia</a>,
and although some of us possibly didn't have awareness for it until 2014 or 2015, the term has been thrown around already for almost a decade.
For the software showcase, we've featured workflow managers quite a bit, and it naturally must come to follow
that we also feature container technologies, which often are the unit of operation passed around by the manager.
In celebration of <a href="https://cloudonair.withgoogle.com/events/singularity_containters_on_gcp_tutorial">Google HPC Cloud Days</a> 
featuring this container technology this week, the RSEPedia software showcase is proud to present <a href="https://github.com/hpcng/singularity" target="_blank">Singularity</a>
for the showcase this week. Singularity, since 2015, has really taken the high performance computing, especially academic,
world by storm by providing a means to run trusted containers on large research clusters with many users.
It's not the only, or a sure fire way to have reproducible science, but it sure is a good contender solution!
Keep reading the following sections to learn more!

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/singularity.png]({{ site.baseurl }}/assets/img/posts/showcase/singularity.png)

<br>

If you are already a container nerd, we encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is Singularity](#what-is)
 - [How do I cite it?](#cite)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is Singularity?

Singularity is a container technology that allows you to package up your operating system, libraries, and
special sauce software into a read only binary that can be shared with your colleagues to reproduce your work.
If you've never used a container before, it sort of feels like shelling into another computer (akin to using ssh)
but it's in fact a container instance running on your machine. Singularity offers:

 - instead of using layers like Docker, a single, single-file based container format that can be signed
 - an ability to work seamlessly with traditional HPC technologies like MPI and filesystems
 - the same entrypoints you would expect from Docker like exec and run, but also shell.
 - an ability to convert from a Docker image right on the fly with the `docker://` unique resource identifier
 - seamless environment with the host as the usual default, unless you specify otherise
 - a large, knowledgeable community.

### Did you know that...

While some of this is old news, here are some fun factoids that you might not have known about Singularity.

#### Founding

Singularity was created by Gregory Kurzer at Berkeley Lab - although unfortunately the punk rock looking site
design is not preserved, you can see the original content on the [wayback machine](https://web.archive.org/web/20160306005043/http://singularity.lbl.gov/) 
(take a look at the favicon to see a glimpse of the branding). It started on his personal GitHub, and was eventually
encouraged to be moved to a more community driven organization, [Singularityware](https://github.com/singularityware), 
which is no longer used. The code base has since moved twice, from [Sylabs](https://github.com/sylabs) and now to [hpcng](https://github.com/hpcng/singularity).
Where will it fly to next?

#### Languages

Did you know that the original Singularity implementation was done in bash, C, and eventually Python? C handled
low level routines, Python handled higher level API communication and parsing functions, and bash tied it all together.
It wasn't until Singularity went under the umbrella of Sylabs that it was fully ported to Go, which of course
adds a lot of benefits over it's previously very-academically appropriate hodge-podge of languages. Take a look at the
[2.x](https://github.com/hpcng/singularity/tree/vault/2.x) branch for a walk down history lane!

#### Docker

Singularity didn't always play nicely with Docker, and in fact it was a contentious feature when it first came under
discussion! An early developer (this writer, @vsoch) advocated for a designed the feature, and added the feature
now [over four years ago](https://github.com/hpcng/singularity/pull/218). Many features that you have come to appreciate
and enjoy that make it feel like Docker came directly from this same route.

#### Forgotten Features

Did you know that an early version of Singularity had a feature called [checks](https://github.com/hpcng/singularity/pull/789)?
Added in summer of 2017, the idea was that the user could run `singularity check <container.sif>` and a series of automated security or other
linting checks would be run, of course under control of the sysadmin managing the install. Although this feature
seemed useful to the developer that implemented it, it was not ported to the Go version of Singularity and is since
lost. However, on a positive note, [the scientific filesystem](https://sylabs.io/guides/3.3/user-guide/cli/singularity_apps.html), 
called Singularity apps, a way to build a container with multiple entrypoints, was carried forward.

Do you have any cool, historical facts to share about Singularity? [Let us know!](https://github.com/rseng/rseng/issues).
Otherwise, if reproducibility is the name of your game, or if you've never tried it before, you should check out <a href="https://sylabs.io/guides/3.5/user-guide/build_a_container.html#creating-writable-sandbox-directories" target='_blank'>Singularity</a>!

<a id="cite">
## How do I cite it?

You can cite the paper from <a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0177459" target="_blank">PLOS One</a>.

```
@article{10.1371/journal.pone.0177459,
    author = {Kurtzer, Gregory M. AND Sochat, Vanessa AND Bauer, Michael W.},
    journal = {PLOS ONE},
    publisher = {Public Library of Science},
    title = {Singularity: Scientific containers for mobility of compute},
    year = {2017},
    month = {05},
    volume = {12},
    url = {https://doi.org/10.1371/journal.pone.0177459},
    pages = {1-20},
    abstract = {Here we present Singularity, software developed to bring containers and reproducibility to scientific computing. Using Singularity containers, developers can work in reproducible environments of their choosing and design, and these complete environments can easily be copied and executed on other platforms. Singularity is an open source initiative that harnesses the expertise of system and software engineers and researchers alike, and integrates seamlessly into common workflows for both of these groups. As its primary use case, Singularity brings mobility of computing to both users and HPC centers, providing a secure means to capture and distribute software and compute environments. This ability to create and deploy reproducible environments across these centers, a previously unmet need, makes Singularity a game changing development for computational science.},
    number = {5},
    doi = {10.1371/journal.pone.0177459}
}
```

There is an <a href="https://ieeexplore.ieee.org/document/6495863/" target="_blank">earlier paper from 2012</a> as well.

<a id="getting-started">
## How do I get started?
 
 - [The Sylabs Documentation](https://sylabs.io/guides/3.5/user-guide/build_a_container.html#creating-writable-sandbox-directories) is a good place to start
 - [Google HPC Days](https://cloudonair.withgoogle.com/events/singularity_containters_on_gcp_tutorial) is featuring a tutorial later this week!
 - [The Singularity Slack](singularity-container.slack.com) has lots of folks to talk to
 - [The Singularity Google Group](https://groups.google.com/a/lbl.gov/forum/embed/#!forum/singularity) is a good place to ask for help.
 
Generally, if you do a GitHub search for Singularity tutorial or getting started, you'll get a robust set of resources, as many
centers have rolled their own getting started guides. You can also post questions on the [GitHub issues board](https://github.com/hpcng/singularity/issues).

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
