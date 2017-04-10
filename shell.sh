#!/bin/bash

export TILER_DATA_DIR=${PWD}/tiler/tiler-data
export TILER_SCRIPTS_DIR=${PWD}/tiler/tiler-scripts

echo “Using this data directory: $TILER_DATA_DIR”
echo “Using this scripts data: $TILER_SCRIPTS_DIR”

docker run -ti -v $TILER_DATA_DIR:/tiler-data -v $TILER_SCRIPTS_DIR:/tiler-scripts -p 25432:5432 tiler --shell