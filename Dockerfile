FROM graphblas/pygraphblas-minimal:v3.3.3

COPY . /graph-database

WORKDIR /graph-database
RUN pip3 install -r requirements.txt