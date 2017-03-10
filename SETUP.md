
## Setup 

Tiler is designed to be easy to use. You create a Docker image and then use commands within the container to convert data to Vector Tiles.

You will require Docker to use Tiler. If you are new to Docker, check this overview [here](https://www.docker.com/what-docker) and see [this link to get hold of it](https://docs.docker.com/engine/getstarted/step_one/#docker-for-mac).

#### Getting the Source
You can use git clone to get the tiler code on your local machine:

`git clone git@github.com:Geovation/tiler.git`

#### Build Docker Image

From the cloned directory you can do:

`docker build -t tiler .`

#### Start Docker Container

You need to specify the location of your data folder so tiler knows where to load data from. We do this using volumes (-v) as such:

`export TILER_DATA_DIR=/Users/username/Documents/Code/tiler/tiler-data` <br>
`export TILER_SCRIPTS_DIR=/Users/username/Documents/Code/tiler/tiler-scripts` <br>

`docker run --name "tiler" \` <br>
            `-v $TILER_DATA_DIR:/tiler-data \ ` <br>
            `-v $TILER_SCRIPTS_DIR:/tiler-scripts \ ` <br>
            `-p 25432:5432 tiler`

There is also a convience script for Linux/MacOS users called `run.sh` that assumes an `export` file (no extension) that lists the TILER_DATA_DIR and TILER_SCRIPTS_DIR in the following format:

`export TILER_DATA_DIR=/Users/username/Documents/Code/tiler/tiler-data` <br>
`export TILER_SCRIPTS_DIR=/Users/username/Documents/Code/tiler/tiler-scripts` <br>

Just replace the paths as appropriate for your scripts and data folders.

#### End Container

`docker stop tiler`

#### Remove Container 

 `docker rm tiler`

## Accessing and Using Tiler

To get into the shell of the Tiler container:

`docker exec -it tiler /bin/bash`
 
Alternatively a convience script for Linux/MacOS users can be run:

 `./shell.sh`

**From here you can begin to run commands given in the usage of the main README**

## Accessing the Postgres Database

If you want to connect via psql from the host you can use:

`psql -h localhost -U docker -p 25432 -l`