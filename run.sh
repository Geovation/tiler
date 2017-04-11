#!/bin/sh
echo "Stopping tiler container if it's still running..."
docker stop tiler
docker rm tiler
export TILER_DATA_DIR=${PWD}/tiler/tiler-data
export TILER_SCRIPTS_DIR=${PWD}/tiler/tiler-scripts
echo "Using the following directories for volume mounting: "
echo "tiler-data : " $TILER_DATA_DIR
echo "tiler-scripts : " $TILER_SCRIPTS_DIR

docker run --name "tiler" \
            -v $TILER_DATA_DIR:/tiler-data \
            -v $TILER_SCRIPTS_DIR:/tiler-scripts \
            -p 25432:5432 \
            tiler $1
            