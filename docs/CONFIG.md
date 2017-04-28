# Config Documentation

Tiler configs are json files that live in the tiler-data/configs. They should be suffixed with `.tiler.json`, for example `someconfig.tiler.json`. 

## Options

Top level config options:

* `outdir` - String - The output directory of the tiles. Required.
* `tileset`  - String - The name of the tile set directory. Required.
* `simplification` - Integer - The level of geometric simplification to use. Defaults to 0 simplifcation.
* `validate` - Boolean - Wether to validate any resulting GeoJSON. Defaults to false.
* `data` - Array - a list of data sets. Required.

The data schema is as follows:

* `type` - String - can be one of `postgis`, `shapefile`, `gml`, `geojson`. Required.

For `type` of `postgis`

* `query` - String - A query string for the geometries you're interested in i.e. SELECT * FROM sometable

For `shapefile`, `gml`, `geojson`:

* `databaseInsert` - Boolean - Should the date be inserted into the specified database beforehand generating the tiles
* `paths` - Array - A array of paths to the data

For both

* `minzoom` - Integer - Minimum zoom level to generate for the tileset
* `maxzoom` - Integer - Maximum zomm level to generate for he tileset


## Example:

```javascript
{

    "outdir" : "/tiler-data/tiles/",
    "tileset" : "states",
    "simplification" : 5,
    "validate" : false,
    "data" : {

        "states" : {
            "type" : "shapefile",
            "databaseInsert" : true,
            "paths" : ["/tiler-data/test-data/states/states.shp"],
            "minzoom" : 0,
            "maxzoom" : 5
        },

        "capitals" : {
            "type" : "postgis",
            "query" : "select * from capitals"
            "minzoom" : 2,
            "maxzoom" : 10
        }

    }

}
```