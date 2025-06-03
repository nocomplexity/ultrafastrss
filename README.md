# Ultra FAST RSS



[![PyPI - Version](https://img.shields.io/pypi/v/ultrafastrss.svg)](https://pypi.org/project/ultrafastrss)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ultrafastrss.svg)](https://pypi.org/project/ultrafastrss)

-----

A simple ASYNC RSS parser. To make retrieving RSS feeds ultra fast.


## Table of Contents

- [Installation](#installation)
- [License](#license)

## Status

> [!CAUTION]
> This is module works and is used! But should be used with care!
Extensive exception validation is left out on purpose for now in the code. 

## Installation

```
pip install ultrafastrss
```


## Usage

In your Python program call the async function with a (large) list of URLs:
`process_rssfeeds(urls)`

To validate and see the working:
Create a simple demo program, create a `python` file  `fastrss_demo.py` like (just copy-paste):
```python
from ultrafastrss.ultrafastrss import process_rssfeeds 
import asyncio

urls = [
        'https://nocomplexity.com/rss',
        'https://www.eff.org/rss/updates.xml',
        'https://www.freebsd.org/news/rss.xml',
        'https://ubuntu.com/blog/feed',
        'https://nlnet.nl/feed.atom',
        'https://j3s.sh/feed.atom',
        'https://blog.research.google/atom.xml'
    ]
    
# Run the async RSS feed processing, all results are as json stored in the variable results

results = asyncio.run(process_rssfeeds(urls))
print(results)
```

After running this demo in a terminal by doing:
```
python ultrafastrss_demo.py
```
You should seen directly the result of all RSS information gathered!

You can do all kind of fun things with the returned `json` object which contains the crucial parts from the parsed `rss` or `atom` feeds!

## Benchmarking

I did some benchmarking test with `feedparser`, a module that is widely used within many Python programs for parsing rss feeds. 
Results are minimal 10 times faster with 500 URLs. 

## License

`ultrafastrss` is distributed under the terms of the [GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.


## Architecture

This ultrafastrss parser is designed to parse `RSS` or `Atom` return JSON data. The parsing is delegating to specific parsers functions (`rss_parser`, `atom_parser` or `rdf_parser`). Only the attributes `title`, `link` and `date` are retrieved. 

The key design principle for this parser is to retrieve JSON data from a significant number of feeds asynchronously. 

Feed content or summary is not parsed on purpose. This is also **not** a RSS reader. But by clicking the retrieved `link`, the retrieved item can be viewed in a browser.

The fields that are parsed and stored for every feed are:

```json
"title": "Exphormer: Scaling transformers for graph-structured data",
      "link": "http://blog.research.google/2024/01/exphormer-scaling-transformers-for.html",
      "date": "2024-01-23",
      "tags": [
        "Deep Learning",
        "Graphs"
```

All kind but edge cases are left out on purpose to keep the needed code simple. Creating a generic module for RSS/ATOM parsing is not simple. So design decision is to only incorporate logic that I need for the URLs I use.


## Contribute

Great you want to contribute!

Simple Guidelines:
* Questions, Feature Requests, Bug Reports please use on the `Github Issue Tracker`.

> [!NOTE]
> This is module works and is used! But it is in pre-release status.
> Extensive exception validation is left out on purpose for now in the code. 
> Feature requests are possible, but will probably only be realized after a quote and paid invoice. But this code is so **Simple** that I encourage everyone to make a special parser and share the code. So we all benefit!



