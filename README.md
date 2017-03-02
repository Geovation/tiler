<img src="tiler.png"><br>
<br>
A Vector Tile Pipeline

### Build Docker Image

`docker build -t tiler .`

### Start Docker Container

You need to specify the location of your data folder so tiler knows where to load data from. We do this using volumes as such:

`docker run --name "tiler" -v /Users/username/Documents/Code/tiler/tiler-data:/tiler-data -p 25432:5432 tiler`

Just replace `/Users/username/Documents/Code/tiler/tiler-data` to the path of your data folder.

### End Container

`docker stop tiler`

### Remove Container 

 `docker rm tiler`

### Usage

To get into shell:

`docker exec -it tiler /bin/bash`

To connect via psql:

`psql -h localhost -U docker -p 25432 -l`

### Credits
Based on Tim Sutton's PostGIS dockerfile.