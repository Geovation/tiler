<img src="tiler.png"><br>
<br>
A Vector Tile Pipeline

The purpose of Tiler is to create an easy to use, command line orientied pipeline for taking vector data in formats such as Shapefiles, and transforming them into raw Vector Tiles and MBTiles files (if required).

Tiler exists as a Docker container that unifies several technologies to streamline the creation of vector tiles.

## Setup 

Tiler is designed to be easy to use. You create a Docker image and then use commands within the container to convert data to Vector Tiles.

#### Build Docker Image

`docker build -t tiler .`

#### Start Docker Container

You need to specify the location of your data folder so tiler knows where to load data from. We do this using volumes (-v) as such:

`docker run --name "tiler" -v /Users/username/Documents/Code/tiler/tiler-data:/tiler-data -p 25432:5432 tiler`

Just replace `/Users/username/Documents/Code/tiler/tiler-data` to the path of your data folder.

#### End Container

`docker stop tiler`

#### Remove Container 

 `docker rm tiler`

## Accessing and Using Tiler

To get into the shell of the Tiler container:

`docker exec -it tiler /bin/bash`
 
Alternatively a convience script can be run:

 `./shell.sh`

## Accessing the Postgres Database

If you want to connect via psql from the host you can use:

`psql -h localhost -U docker -p 25432 -l`

## License

MIT Licensed - see LICENSE.txt