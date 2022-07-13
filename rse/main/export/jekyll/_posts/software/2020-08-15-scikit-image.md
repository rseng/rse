---
layout: post
title: "Scikit-image"
date: 2020-08-15 08:30:46
author: "@vsoch"
annotate_criteria: https://rseng.github.io/software/repository/github/scikit-image/scikit-image/annotate-criteria/
annotate_taxonomy: https://rseng.github.io/software/repository/github/scikit-image/scikit-image/annotate-taxonomy/
categories:
- Software
---

This week the software showcase is celebrating image processing! While there are many domains that use it, and many
software packages and languages to help, this week we celebrate <a href="https://scikit-image.org/" target="_blank">scikit-image</a>,
which has you covered for many algorithms, tutorials, and examples.

<br>

![{{ site.baseurl }}/assets/img/posts/showcase/scikit-image.png]({{ site.baseurl }}/assets/img/posts/showcase/scikit-image.png)

<br>

If you already know about scikit-image, we encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is Scikit Image?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)


<a id="what-is">
## What is Scikit Image?

According to the first page of the website, scikit-image embodies all the lovely bits about open source and community
that we generally value in open source development:

> scikit-image is a collection of algorithms for image processing. It is available free of charge and free of restriction. We pride ourselves on high-quality, peer-reviewed code, written by an active community of volunteers.

The site also mentions that it builds on scipy's <a href="https://docs.scipy.org/doc/scipy/reference/ndimage.html" target="_blank">ndimage</a>,
and according to the [scipy website](https://www.scipy.org/about.html), it's part of the Scipy ecosystem as well. Which came first?
If we go by the mailing list, the scipy-dev and scipy-users mailing list both had their first test message in [June 2001](https://mail.python.org/pipermail/scipy-user/2001-June/thread.html). On the other hand, scikit-learn's mailing list came to life much later, in
[September of 2009](https://mail.python.org/archives/list/scikit-image@python.org/thread/SRB7EEQTAFAZSIQPAOKCZHBY47RMNM5O/).
This also gives us a bit of insight about [it's development](https://mail.python.org/archives/list/scikit-image@python.org/thread/3SQ4UOGRXBOFJJGGR22TU7LPW6UFESBN/). How do you ultimately develop a large, successful, and highly useful library for image processing and Python?

![{{ site.baseurl }}/assets/img/posts/showcase/scikit-image-mailing-list.png]({{ site.baseurl }}/assets/img/posts/showcase/scikit-image-mailing-list.png)

If we guess from the early posts, you need a community of people that deeply care about creating and maintaining a useful
library. In the image above, we see organization by way of:

 - having discussion at a meetup / sprint
 - creating a mailing list
 - version control a la GitHub
 - documentation
 - calls for contribution

And it looks like by the end of 2012 (a little over a year) the project had ben renamed from `scikits.image` to `scikit-image` and even moved
over to a community repository, where it lives now.

![{{ site.baseurl }}/assets/img/posts/showcase/scikit-image-moved.png]({{ site.baseurl }}/assets/img/posts/showcase/scikit-image-moved.png)

I highly encourage you to explore the beginning posts for this library on the [mailing list archives](https://mail.python.org/archives/list/scikit-image@python.org/2009/9/)! It's very organically grown, e.g.,

> I know a friend has some filtered back-projection code which may still be based on numarray, but is apparently quite fast. I'll try to get him to contribute it (and numpyify it first if necessary).  - Gary Ruben (mailing list post from 2009)

And I bet that the community has maintained it's open and welcoming values. For example, there was a [sprint](https://mail.python.org/archives/list/scikit-image@python.org/thread/AJAHLYA6ZOCXHUOPJXEIRHLMFLBSSZ42/) advertised for the end of July. Also, check out the [mission](https://scikit-image.org/docs/stable/values.html) that is clearly stated on the site. If other projects need inspiration, here it is!


<a id="cite">
## How do I cite it?

You can cite [this article](https://doi.org/10.7717/peerj.453) published in PeerJ in 2014:

```
Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014) https://doi.org/10.7717/peerj.453 
```

and here is the corresponding BibTeX entry:
```
@article{scikit-image,
 title = {scikit-image: image processing in {P}ython},
 author = {van der Walt, {S}t\'efan and {S}ch\"onberger, {J}ohannes {L}. and
           {Nunez-Iglesias}, {J}uan and {B}oulogne, {F}ran\c{c}ois and {W}arner,
           {J}oshua {D}. and {Y}ager, {N}eil and {G}ouillart, {E}mmanuelle and
           {Y}u, {T}ony and the scikit-image contributors},
 year = {2014},
 month = {6},
 keywords = {Image processing, Reproducible research, Education,
             Visualization, Open source, Python, Scientific programming},
 volume = {2},
 pages = {e453},
 journal = {PeerJ},
 issn = {2167-8359},
 url = {https://doi.org/10.7717/peerj.453},
 doi = {10.7717/peerj.453}
}
```

<a id="getting-started">
## How do I get started?

You might visit any of the following links!

 - [The GitHub Repository](https://github.com/scikit-image/scikit-image) gets you right into install, and usage.
 - [The Gallery](https://scikit-image.org/docs/stable/auto_examples/index.html) is my favorite place to explore, because I can see what I might do.
 - [The Documentation Site](https://scikit-image.org/docs/stable/) let's you browse documentation topics that fit your needs
 - [The First Blog Post](https://ilovesymposia.com/2018/07/13/the-road-to-scikit-image-1-0/) in 2018 that shared the road behind and the road ahead.
 - [Discussion](https://github.com/scikit-image/scikit-image/issues/3263) of the first blog post on a GitHub issue.

You can also post questions on the [GitHub issues board](https://github.com/scikit-image/scikit-image/issues).


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
