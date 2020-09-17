FROM graphblas/pygraphblas-minimal:latest

COPY . /graph-database

WORKDIR /graph-database
RUN pip3 install -r requirements.txt