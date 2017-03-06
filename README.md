<img src="tiler.png"><br>
<br>
A no nonsense Vector Tile pipeline

The purpose of Tiler is to create an easy to use, command line orientied pipeline for taking vector data in formats such as Shapefiles, and transforming them into raw Vector Tiles and MBTiles files (if required).

Tiler exists as a Docker container that unifies several technologies to streamline the creation of vector tiles.

## Setup 

Tiler is designed to be easy to use. You create a Docker image and then use commands within the container to convert data to Vector Tiles.

You will require Docker to use Tiler. If you are new to Docker, check this overview [here](https://www.docker.com/what-docker) and see [this link to get hold of it](https://docs.docker.com/engine/getstarted/step_one/#docker-for-mac).

#### Build Docker Image

`docker build -t tiler .`

#### Start Docker Container

You need to specify the location of your data folder so tiler knows where to load data from. We do this using volumes (-v) as such:

`export TILER_DATA_DIR=/Users/username/Documents/Code/tiler/tiler-data` <br>
`export TILER_SCRIPTS_DIR=/Users/username/Documents/Code/tiler/tiler-scripts` <br>

`docker run --name "tiler" \
            -v $TILER_DATA_DIR:/tiler-data \
            -v $TILER_SCRIPTS_DIR:/tiler-scripts \
            -p 25432:5432 tiler`

Just replace the paths as appropriate for your scripts and data forlders.

#### End Container

`docker stop tiler`

#### Remove Container 

 `docker rm tiler`

## Accessing and Using Tiler

To get into the shell of the Tiler container:

`docker exec -it tiler /bin/bash`
 
Alternatively a convience script can be run:

 `./shell.sh`

#### Using Tiler

WARNING: Work in Progress! Eventually these commands will be bundled together to make an even smoother transition from geo formats to Vector Tiles.

Current scripts:

`python geojson2tiles.py` <br>
`python postgis2geojson.py` <br>
`python shapefile2postgis.py` <br>
`python geojson2tiles.py` <br>

### Tests

`cd tiler-scripts` <br>
`nosetests`

#### Demo Vector Tile 

Demos are provided using [Leaflet.VectorGrid](http://leaflet.github.io/Leaflet.VectorGrid/vectorgrid-api-docs.html) and also [Mapbox GL](https://www.mapbox.com/mapbox-gl-js/api/) for you to display your tiles when you're done.

## Accessing the Postgres Database

If you want to connect via psql from the host you can use:

`psql -h localhost -U docker -p 25432 -l`

## License

MIT License