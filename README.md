<table>
<tr>
<th>
dev
</th>
<th>
master
</th>
</tr>
<tr>
<td>

[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=dev)](https://travis-ci.com/viabzalov/graph-database)

</td>
<td>

[![Build Status](https://travis-ci.com/viabzalov/graph-database.svg?branch=master)](https://travis-ci.com/viabzalov/graph-database)

</td>
</tr>
</table>

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

# Database query syntax

## Usage
```bash
usage: checker.py [-h] [--script SCRIPT]

script validator

optional arguments:
  -h, --help       show this help message and exit
  --script SCRIPT  path to script.txt file
```

## Syntax
```bash
Script -> (Statement) (Statement*)
Statement -> Connect To Database Address ;
Statement -> Select Result From Graph ;
Statement -> Select Result From Graph Where Query ;
Graph -> Intersection Of Graph And Graph
Graph -> Word
Query -> Word
Query -> ( \( ) Word ( \) )
Query -> ( \( ) Query ( \* ) ( \) )
Query -> ( \( ) Query ( \| ) Query ( \) )
Query -> ( \( ) ( \( ) Query ( \) ) ( \( ) Query ( \) ) ( \) )
Intersection -> i n t e r s e c t i o n
Of -> o f
And -> a n d
Result -> p a i r s
Result -> c o u n t
Select -> s e l e c t
From -> f r o m
Where -> w h e r e
Connect -> c o n n e c t
To -> t o
Database -> d a t a b a s e
Address -> ((Word | /)) ((Word | /)*)
Word -> (Symbol) (Symbol)*
Symbol -> (a|(b|(c|(d|(e|(f|(g|(h|(i|(j|(k|(l|(m|(n|(o|(p|(q|(r|(s|(t|(u|(v|(w|(x|(y|(z|(0|(1|(2|(3|(4|(5|(6|(7|(8|(9|_))))))))))))))))))))))))))))))))))))
```

## Examples

```
connect to database resources/database_1 ;
select pairs from g1 ;
select count from g2 where (((a|b)|(c*))*) ;
```

```
connect to database resources_database_42 ;
select pairs from intersection of g1 and g2 where ((a*)|(b*)) ;
```

```
python3 checker.py --script example_script.txt

# Benchmark RPQ

In order to run benchmarks you need a [dataset](https://drive.google.com/file/d/19L7RUCJlkgWQpQRnp6hMb7MLXibB4jTp/view?usp=sharing). 
You can download the dataset using gdown or manually from Google Drive.
All this can be done by 
* running the script `benchmark_rpq.sh` 
* or by using docker ```docker run -it --rm -p 8787:8787 viabzalov/pygraphblas-database:latest python3 -m pytest -v -s benchmarks/benchmark_rpq/test_benchmark_rpq.py```

Results obtained on a computer with OS Ubuntu 20.04, Intel core i7-4790 CPU 3.60 GHz, DDR3 32Gb RAM on graphs [`LUBM300`, `LUBM500`, `LUBM1M`, `LUBM1.5M`] showed that there is no difference between linear and quadratic algorithms for calculating transitive closure

More detailed results can be found in `benchmarks/benchmark_rpq/results/analytics.ipynb` or `benchmarks/benchmark_rpq/results/analytics.pdf`

# Benchmark CFPQ

In order to run benchmarks you need a [dataset](https://drive.google.com/file/d/1lF20sF9-HmUoErdV2Z6VkFjpzdugOuC0/view?usp=sharing). 
You can download the dataset using gdown or manually from Google Drive.
All this can be done by 
* running the script `benchmark_cfpq.sh` 

Results obtained on a computer with OS Ubuntu 20.04, Intel core i7-4790 CPU 3.60 GHz, DDR3 32Gb RAM on graphs ['FullGraph', 'WorstCase', 'MemoryAliases'] showed that Azimov's matrix-based algorithm is the best choice for CFPQ evaluation

More detailed results can be found in `benchmarks/benchmark_cfpq/results/analytics.ipynb`
