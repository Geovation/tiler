echo "Stopping tiler container if it's still running..."
docker stop tiler
docker rm tiler
. export 
echo "Using the following directories: "
echo $TILER_DATA_DIR
echo $TILER_SCRIPTS_DIR
docker run --name "tiler" \
            -v $TILER_DATA_DIR:/tiler-data \
            -v $TILER_SCRIPTS_DIR:/tiler-scripts \
            tiler $1