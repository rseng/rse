---
layout: post
title: "AstroPaint"
date: 2020-11-08
author: "@tabakg"
annotate_criteria: https://rseng.github.io/software/repository/github/syasini/AstroPaint/annotate-criteria/index.html
annotate_taxonomy: https://rseng.github.io/software/repository/github/syasini/AstroPaint/annotate-taxonomy/
categories:
- Software
---


<br>

![{{ site.baseurl }}/assets/img/posts/showcase/astropaint.png]({{ site.baseurl }}/assets/img/posts/showcase/astropaint.png)

<br>

Do you have an opinion? We encourage you to contribute to the [research software encyclopedia](https://rseng.github.io/rse/tutorials/annotation/) and annotate the respository:

<ul>
<li><a href="{{ page.annotate_criteria }}" target="_blank">Annotate the software criteria</a></li>
<li><a href="{{ page.annotate_taxonomy }}" target="_blank">Annotate the software taxonomy</a></li>
</ul>

otherwise, keep reading!

<!--more--> 

 - [What is AstroPaint?](#what-is)
 - [How do I cite it?](#cite)
 - [How do I get started?](#getting-started)
 - [How do I contribute to the software survey](#contribute)
 - [Where can I learn more?](#learn-more)

<a id="what-is">
## What is AstroPaint?

First, let's talk about the [Cosmic Microwave Background](https://en.wikipedia.org/wiki/Cosmic_microwave_background) (CMB). This is a faint signal we can detect in all directions from space, which is believed to originate with the early universe. Astrophysicists have tried to come up with models for the universe that are aligned with observations of the CMB to improve our understanding of the universe.

AstroPaint generates mock maps of astrophysical signals based on catalogs of [dark matter halos](https://en.wikipedia.org/wiki/Dark_matter_halo). These represent clusters of matter in the universe that are gravitationally bound together.

It also generates very cool-looking 'artwork' -- with some components that can even be run [in a browser](https://astropaint-art-gallery.herokuapp.com/).


#### Why is it useful?

AstroPaint uses a numerically affordable strategy of painting various signals at the location of 'extended objects' (e.g., galaxies) to help astrophysicists studying the universe at a large scale. In typical studies it is important to simulate various effects as well as the background noise from other objects to understand our observations. One example AstroPaint's paper cites is the Birkinshaw-Gull effect: When objects move in the transverse direction (along the plane of the image), we may expect to see a difference in the amount of gravitational lensing (how the gravity of closer objects impact how we see farther objects by bending light). They show this example in [a notebook](https://github.com/syasini/AstroPaint/blob/master/examples/Birkinshaw_Gull_stacking.ipynb). Very cool!


<a id="cite">
## How do I cite it?

There is an accompanying paper, which you can cite using:

```
@article{Yasini2020,
  doi = {10.21105/joss.02608},
  url = {https://doi.org/10.21105/joss.02608},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {55},
  pages = {2608},
  author = {Siavash Yasini and Marcelo Alvarez and Emmanuel Schaan and Karime Maamari and Shobeir K. s. Mazinani and Nareg Mirzatuny and Elena Pierpaoli},
  title = {AstroPaint: A Python Package for Painting Halo Catalogs into Celestial Maps},
  journal = {Journal of Open Source Software}
}

```

<a id="getting-started">
## How do I get started?
 
 - [README Documentation](https://github.com/syasini/AstroPaint) is always a good place to start.
 - [In-browser mock maps](https://astropaint-art-gallery.herokuapp.com/).
 - [JOSS paper](https://www.theoj.org/joss-papers/joss.02608/10.21105.joss.02608.pdf).

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
