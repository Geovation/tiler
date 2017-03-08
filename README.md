<img src="tiler.png"><br>
<br>
A no nonsense Vector Tile pipeline

The purpose of Tiler is to create an easy to use, command line orientied pipeline for taking vector data in formats such as Shapefiles, and transforming them into raw Vector Tiles and MBTiles files (if required).

Tiler exists as a Docker container that unifies several technologies to streamline the creation of vector tiles.

#### Setup

Setup requires installation of Docker and a few Docker commands to get started. We've provided a nice little set of instructions in the [SETUP](https://github.com/Geovation/tiler/blob/master/SETUP.md) file.

#### Using Tiler

Tiler provides a selection of scripts for converting between various formats and validating them (see the tiler-scripts folder). The primary and simplest way to use Tiler however is to use a config file placed in `tiler-data/configs`:


```javascript
{

    "outdir" : "/tiler-data/tiles/",
    "tileset" : "states",
    "simplification" : 5,
    "data" : {

        "states" : {
            "type" : "shapefile",
            "paths" : ["/tiler-data/test-data/states/states.shp"],
            "minzoom" : 0,
            "maxzoom" : 4
        }

    }

}
```

This would be saved as `tiler-data/configs/states.tiler.json`. The file provides the location of the files you wish to translate, along with the output directory and if you want any simplification to occur. "data" is an object full of layers you wish to be ingested into the tiles. Each data layer can have multiple files that they use to generate that layer ("paths"). You can also provide a minimum zoom ("minzoom") and a maximum zoom ("maxzoom") for each layer.

You can then use 

`python /tiler-scripts/tiler.py states`

To generate the set of uncompressed vector tiles and an .mbtiles file.

### Tests

A set of tests are provided that can be run using [nosetest](http://nose.readthedocs.io/en/latest/):

`cd tiler-scripts` <br>
`nosetests -v`

#### Demo Vector Tile 

Demos are provided using [Leaflet.VectorGrid](http://leaflet.github.io/Leaflet.VectorGrid/vectorgrid-api-docs.html) and also [Mapbox GL](https://www.mapbox.com/mapbox-gl-js/api/) for you to display your tiles when you're done. You will need to specify your own styling in these examples.

## Accessing the Postgres Database

If you want to connect via psql from the host you can use:

`psql -h localhost -U docker -p 25432 -l`

## Credits

This project was made possible thanks to building on a fantastic set of previous previous software:

* [mbutil](https://github.com/mapbox/mbutil) - Mapbox 
* [tippecanoe](https://github.com/mapbox/tippecanoe) - Mapbox 
* [ogr2ogr](http://www.gdal.org/ogr2ogr.html) - OSGeo 
* [PostGIS Docker Container](https://github.com/kartoza/docker-postgis) - Tim Sutton

## License

MIT License