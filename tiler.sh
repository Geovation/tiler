#!/bin/bash
echo "Waiting for database to setup"

./postgis/start-postgis.sh &> /dev/null &

setup=0
while [ $setup == 0 ]
do
    sleep 1
    echo -n "."
    if sudo -u postgres psql -lqt 2> /dev/null | cut -d \| -f 1 | grep -qw gis; then
        echo "\n TILER: Database is ready for tests!"
        setup=1
    fi
done

if [ "$1" == "--help" ] || [ -z "$1" ]; then
    echo "To use tiler pass in the name of a config file from the config directory"
    echo "E.g. for a config file named example.tiler.json, you would do: tiler example"
elif [ "$1" == '--test' ] || [ "$1" == '--tests' ]; then
    echo "Excuting tests..."
    nosetests /tiler-scripts/ -xs "$2"
else
    echo "Running config : " + "$1"
    python /tiler-scripts/tiler.py "$1"
fi