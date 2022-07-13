---
layout: post
title: "Easybuild"
date: 2020-09-20 08:30:46
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/easybuilders/easybuild/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/easybuilders/easybuild/annotate-taxonomy/
categories:
- Software
---

Installing software from source is a non-trivial problem. That's why we are a huge fan of package managers
at the RSEpedia software showcase, and why this week we are featuring <a href="https://github.com/easybuilders/easybuild" target="_blank">easybuild</a>. Easybuild is especially pertinent to the research community because it's intended
to install and manage scientific software on High Performance Computing (HPC) resources. Keep reading the following
sections to learn more!

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/easybuild.png]({{ site.baseurl }}/assets/img/posts/showcase/easybuild.png)

<br>

If you are already an easybuilder, we encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is Easybuild](#what-is)
 - [How do I cite it?](#cite)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is Easybuild?

Let's say you're an HPC administrator. Or maybe you're a researcher that has found himself unexpectedly as
manager of a few servers. You likely have an entire suite of scientific software packages that you
want to provide to your user base, whether that be a small group like a lab or an entire academic center. 
You likely have different versions too, and subtle differences in dependencies. What to do? While you might decide that <a href="https://lmod.readthedocs.io/en/latest/" target="_blank">environment modules</a> 
are the way to go, or perhaps a previous week's package manager, <a href="https://rseng.github.io/rseng/software/spack" target="_blank">spack</a>,
easybuild offers a set of features that might whet your appetite:

 - fully automated, reproducible software builds with dependency resolution
 - custom install procedures (instead of traditional configure, make, make install)
 - co-existence of different versions via dedicated installation prefixes and module files
 - build recipes are simple and human readable (this is a huge deal!)
 - sharing of recipes within the HPC community
 - logs are kept as a record of the build process
 - install in parallel, if desired
 - a thriving, growing community.

The last point about community is a big deal! It means that if you use easybuild and need help, there are <a href="https://easybuild.readthedocs.io/en/latest/Maintainers.html" target="_blank">many
others</a> that are able and willing to help you. Here is a group picture from the 5th EasyBuild User Meeting, 
held in Jan 2020. Yes, right before the coronapocalypse!

![{{ site.baseurl }}/assets/img/posts/showcase/easybuild-community.png]({{ site.baseurl }}/assets/img/posts/showcase/easybuild-community.png)

In terms of software supported, check out the list of <a href="https://easybuild.readthedocs.io/en/latest/version-specific/Supported_software.html" target="_blank">supported software</a> - there are over 2000! 
But don't take our word for it! The easybuild documentation has a <a href="https://easybuild.readthedocs.io/en/latest/Introduction.html" target="_blank">What is easybuild?</a> page that can tell you more.

<a id="cite">
## How do I cite it?

While there isn't a recommended paper to cite in the repository, you can likely reference <a href="https://dl.acm.org/doi/10.1109/HUST.2014.8" target="_blank">this ACM publication</a>:

```
@inproceedings{10.1109/HUST.2014.8,
author = {Geimer, Markus and Hoste, Kenneth and McLay, Robert},
title = {Modern Scientific Software Management Using EasyBuild and Lmod},
year = {2014},
isbn = {9781467367554},
publisher = {IEEE Press},
url = {https://doi.org/10.1109/HUST.2014.8},
doi = {10.1109/HUST.2014.8},
abstract = {HPC user support teams invest a lot of time and effort in installing scientific software for their users. A well-established practice is providing environment modules to make it easy for users to set up their working environment. Several problems remain, however: user support teams lack appropriate tools to manage a scientific software stack easily and consistently, and users still struggle to set up their working environment correctly. In this paper, we present a modern approach to installing (scientific) software that provides a solution to these common issues. We show how EasyBuild, a software build and installation framework, can be used to automatically install software and generate environment modules. By using a hierarchical module naming scheme to offer environment modules to users in a more structured way, and providing Lmod, a modern tool for working with environment modules, we help typical users avoid common mistakes while giving power users the flexibility they demand.},
booktitle = {Proceedings of the First International Workshop on HPC User Support Tools},
pages = {41–51},
numpages = {11},
location = {New Orleans, Louisiana},
series = {HUST '14}
}
```

There is an <a href="https://ieeexplore.ieee.org/document/6495863/" target="_blank">earlier paper from 2012</a> as well.

<a id="getting-started">
## How do I get started?

 - [The EasyBuild tutorial](https://easybuilders.github.io/easybuild-tutorial/) is a great place to start. It was intended to be in-person at ISC'20, but COVID-19 mucked up that plan. The easybuilders community persisted anyway! It was held 100% virtually, and hugely successful, with close to 100 participants. The exercises are quick and useful, as there is a <a href="https://easybuilders.github.io/easybuild-tutorial/practical_information/#prepared-container-image" target="_blank">container image</a> provided to get you up and running! Not only are there working cases to learn from, but also debugging challenges.
 - [Easybuild Tech Talks](https://github.com/easybuilders/easybuild/wiki/EasyBuild-Tech-Talks) might you learn watching something over dinner? EasyBuild has started a small series of tech talks that currently include the topics of Arm and Open MPI, the first of which is still coming up on September 30th!
 - [Kenneth Hoste on RSE Stories](https://us-rse.org/rse-stories/2020/kenneth-hoste/): if you want to snuggle into a warm chair and listen to learn, you might be interested in listening to Kenneth talk about easybuild on the Research Software Engineer Stories Podcast.
 - [The EESSI Project](https://eessi.github.io/docs): pronounced "easy," this project grown out of the easybuild community aims to build a ready-to-go stack of properly optimized software installations for HPC systems, cloud, and workstations. It's heavily inspired by the <a href="https://www.computecanada.ca/" target="_blank">Compute Canada</a> software stack. See maintainer Kenneth Hoste's <a href="https://www.youtube.com/watch?v=E0LFvrZIsi8" target="_blank">introduction to the project</a> video, and if you're super eager, jump right into the <a href="https://eessi.github.io/docs/pilot/">pilot</a>.
 - [How to Make Package Mangers Cry](https://www.youtube.com/watch?v=NSemlYagjIU) if you want an introduction to some of the problems of package management, and a good laugh.
 - [Kenneth Hoste on Twitter](https://twitter.com/kehoste) and [Easybuild on Twitter](https://twitter.com/easy_build) if you want a quick ping for social media. 
 
You can also post questions on the [GitHub issues board](https://github.com/easybuilders/easybuild/issues).

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
