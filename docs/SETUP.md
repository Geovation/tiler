
## Setup 

Tiler is designed to be easy to use. You create a Docker image and then use commands within the container to convert data to Vector Tiles.

You will require Docker to use Tiler. If you are new to Docker, check this overview [here](https://www.docker.com/what-docker) and see [this link to get hold of it](https://docs.docker.com/engine/getstarted/step_one/#docker-for-mac).

#### Getting the Source
You can use git clone to get the tiler code on your local machine:

`git clone git@github.com:Geovation/tiler.git`

#### Build Docker Image

```
cd tiler
docker build -t tiler .
```

#### Start Docker Container

The simplest way to run Tiler interactively is to use the `run.sh` script which handles most things for you (volume mounting etc), which takes the arguments: 

`./run.sh --shell`

At this point you will be in the container. You could run:

`tiler someconfig`

From the root folder to creat tiles for the `someconfig` config file.

## Accessing and Using Tiler

All the above assumes you are on the host machine, in the tiler root directory.

You can run a config that you have described using the following command from the host machine:

`./run.sh someconfig`

Where someconfig is a config file with the path `tiler/tiler-data/configs/someconfig.tiler.json`.  

You can also run tests from the host machine using:

`./run.sh --test`

As previously mentioned to access Tiler in an interactive mode you can run:

 `/run.sh --shell`

This will allow you to run scripts that you want individually.

Alternatively you can use for a more explicit approach you could use individual commands. You need to specify the location of your data folder so tiler knows where to load data from. We do this using volumes (-v) as such:

```
export TILER_DATA_DIR=/Users/username/Documents/Code/tiler/tiler-data
export TILER_SCRIPTS_DIR=/Users/username/Documents/Code/tiler/tiler-scripts
```

```
docker run --name "tiler" \
-v $TILER_DATA_DIR:/tiler-data \
-v $TILER_SCRIPTS_DIR:/tiler-scripts \
-p 25432:5432 tiler --shell
```       

You need to replace the export paths with your tiler-data and tiler-scripts paths.

#### End Container

`docker stop tiler`

#### Remove Container 

 `docker rm tiler`

**From here you can begin to run commands given in the usage of the main [README](https://github.com/Geovation/tiler/blob/master/README.md)**

## Accessing the Postgres Database

If you want to connect via psql from the host you can use:

`psql -h localhost -U docker -p 25432 -l`
