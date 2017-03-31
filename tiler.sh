#!/bin/sh

if [ "$1" = "--help" ] || [ -z "$1" ]; then
    echo "To use tiler pass in the name of a config file from the config directory"
    echo "E.g. for a config file named example.tiler.json, you would do: tiler example"
elif [ "$1" = '--test' ]; then
    echo "Excuting tests..."
    nosetests /tiler-scripts/ -xs
else
    echo "Running config : " + $1
    python /tiler-scripts/tiler.py $1
fi