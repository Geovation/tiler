#!/bin/bash

./postgis/start-postgis.sh &> /dev/null &

start_database()
{
    echo "Waiting for database to setup"
    setup=0
    while [ $setup == 0 ]
    do
        sleep 1
        echo -n "."
        if sudo -u postgres psql -lqt 2> /dev/null | cut -d \| -f 1 | grep -qw gis; then
            echo ""
            setup=1
        fi
    done

    echo "\n TILER: Database is ready for tests!"
}

if [ "$1" == "--help" ] || [ -z "$1" ]; then
    echo "To use tiler pass in the name of a config file from the config directory"
    echo "E.g. for a config file named example.tiler.json, you would do: tiler example"

elif [ "$1" == '--test' ] || [ "$1" == '--tests' ]; then
    start_database
    echo "Excuting tests..."
    nosetests /tiler-scripts/ -xs "$2"

elif [ "$1" == '--shell' ]; then
    start_database
    echo "Running shell..."
    /bin/bash

else
    echo "Running config : " + "$1"
    start_database
    python /tiler-scripts/tiler.py "$1"
fi