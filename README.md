[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=dev)](https://travis-ci.com/viabzalov/graph-database)
[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=master)](https://travis-ci.com/viabzalov/graph-database)

# graph-database
Simple graph database on Python

# Install

This project uses miniconda to download and install packages, if you don't have it installed, the installation script will download and install it itself.

To run the installation script, execute the command.

```bash
git clone https://github.com/viabzalov/graph-database.git
cd graph-database
./install.sh
```

And, after that, restart the terminal.

# Using Docker

An alternative way of building and running tests is using Docker container.

```bash
# build docker image
docker build -t graph-database .

# run docker container
docker run -it --rm -v "$PWD":/graph-database graph-database python3 main.py
```

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