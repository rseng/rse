# CHANGELOG

This is a manually generated log to track changes to the repository for each release.
Each section should include general headers such as **Implemented enhancements**
and **Merged pull requests**. Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes
 - migration guidance
 - changed behaviour

The versions coincide with releases on pip.

## [0.0.x](https://github.com/rseng/rse/tree/master) (0.0.x)
 - ensure Google scraper skips malformed rows, etc (0.0.45)
 - Logging bugs and adding export/import docs (0.0.44)
 - Adding debian-med scraper (0.0.43)
 - Bug in biogrids to output github.com URI (0.0.42)
 - Template style bug fixes (0.0.41)
 - Adding biogrids scraper (0.0.40)
 - additional scrapers from https://scicodes.net/, ascl (0.0.39)
 - adding custom jekyll exporter for static site (0.0.38)
   - support for custom parser and import from Google Sheet
   - custom topics from sheets in column "tags" and comma separated
   - import can have `--update` to indicate updating an existing record.
 - import bug (0.0.37)
 - adding imperial college london research software directory (0.0.36)
 - adding molssi scraper (0.0.35)
 - adding ropensci scraper (0.0.34)
 - updating local index to be a data table (0.0.33)
 - move repository link to be part of card (0.0.32)
 - ipython should not be required for shell (0.0.31)
 - updating annotation interface to be better searched (0.0.30)
 - adding topics to GitHub request (0.0.29)
 - scraper should not fail on invalid URL (0.0.28)
 - bug with reading in taxonomy lines (0.0.27)
 - bug in github parser (0.0.26)
 - refactoring interface to have one column table (0.0.24)
 - streamline data export to included minimal repo data (0.0.23)
 - static search interface and delay parameter for scrape (0.0.22)
 - ensuring that interface generation uses constent colors (0.0.21)
 - bug that taxonomy needs newline for export (0.0.2)
 - adding analysis metrics (0.0.19)
 - bugfix to export json api including url prefix 0.0.18)
 - static annotation export to GitHub issues (0.0.17)
 - allowing Zenodo parser to hand off to GitLab or GitHub (0.0.16)
 - adding import of static issue (markdown) files for annotation (0.0.15)
 - adding generation of data.json to static site export (0.0.14)
 - web interface needs software (or other custom) prefix for export (0.0.13) 
 - Adding export of flask for static interface (0.0.12)
 - Updating beautiful soup to use html.parser (0.0.11)
 - first draft including database backends and GitHub parser (0.0.1)
 - skeleton release (0.0.0)
