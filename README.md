# graph-database
Simple graph database on Python

# CI

[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=dev)](https://travis-ci.com/viabzalov/graph-database)
[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=master)](https://travis-ci.com/viabzalov/graph-database)

# Install

This project uses miniconda to download and install packages, if you don't have it installed, the installation script will download and install it itself.

To run the installation script, execute the command:

```bash
./install.sh
```

And, after that, restart the terminal.

# How to use

Only non-empty graphs and non-empty queries are supported.

```
usage: main.py [-h] --graph GRAPH --query QUERY [--sources SOURCES]
               [--destinations DESTINATIONS]

command line interface for simple graph database

optional arguments:
  -h, --help            show this help message and exit
  --graph GRAPH         path to graph.txt file
  --query QUERY         path to query.txt file
  --sources SOURCES     path to sources.txt file
  --destinations DESTINATIONS
                        path to destinations.txt file

```