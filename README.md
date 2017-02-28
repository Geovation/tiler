# Tiler: A Vector Tile Pipeline

### Build Docker Image

docker build -t tiler .

### Start Docker Container

You need to specify the tiler folder when you run the docker command so it knows the location of the scripts and your data.

docker run --name "tiler" -v /Users/username/Documents/Code/tiler/tiler-data:/tiler-data -p 25432:5432 tiler

### End Container

docker stop tiler

### Usage

To get into shell:

docker exec -it tiler /bin/bash

To connect via psql:

psql -h localhost -U docker -p 25432 -l

### Credits
Based on Tim Sutton's PostGIS dockerfile.