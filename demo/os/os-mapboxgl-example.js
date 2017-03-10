
var vectortiles = "os";
var PORT = "8080";
var HOST = "http://127.0.0.1";
var url = HOST + ":"+ PORT + "/tiler/tiler-data/tiles/"+vectortiles+"/{z}/{x}/{y}.pbf";
console.log(url);

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNtaWxuZXIiLCJhIjoiY2lsMm96djd1MDBjYndnbTVmajAxeHByaiJ9.mw4lltZ8qZjJHaJwbnN5Yw';

var tilelayers = [
    {
        "id": "buildings",
        "type": "fill",
        "source": "os",
        "minzoom": 5,
        "source-layer": "buildings",
        "filter": ["==", "$type", "Polygon"],
        "paint": {
            "fill-color": "rgba(240,11,11, 0.2)"
        }
    },
    {
        "id": "roads",
        "type": "line",
        "source": "os",
        "minzoom": 5,
        "source-layer": "roads",
        // "filter": ["==", "$type", "Line"],
        "paint": {
            "line-color": "rgba(11,11,11, 0.4)"
        }
    },

    {
        "id": "roadtunnel",
        "type": "line",
        "source": "os",
        "source-layer": "roadtunnel",
        "minzoom" : 8,
        "maxzoom" : 14,
        "paint": {
            "line-color": "rgba(11,240,240, 0.2)"
        }
    },

    {
        "id": "roundabout",
        "type": "line",
        "source": "os",
        "source-layer": "roundabout",
        "minzoom" : 8,
        "maxzoom" : 14,
        "paint": {
            "line-color": "rgba(240,11,240, 0.2)"
        }
    },

    {
        "id": "surfacewater",
        "type": "fill",
        "source": "os",
        "source-layer": "surfacewater",
        "minzoom" : 0,
        "maxzoom" : 14,
        "paint": {
            "fill-color": "rgba(11,11,200, 0.1)"
        }
    },

    {
        "id": "tidalboundary",
        "type": "line",
        "source": "os",
        "source-layer": "tidalboundary",
        "minzoom" : 0,
        "maxzoom" : 14,
         "paint": {
            "line-color": "rgba(11,11,200, 0.2)"
        }
    },

    {
        "id": "tidalwater",
        "type": "fill",
        "source": "os",
        "source-layer": "tidalwater",
        "minzoom" : 0,
        "maxzoom" : 14,
         "paint": {
            "fill-color": "rgba(11,11,200, 0.2)"
        }
    },

    {
        "id": "woodland",
        "type": "fill",
        "source": "os",
        "source-layer": "woodland",
        "minzoom" : 4,
        "maxzoom" : 14,
         "paint": {
            "fill-color": "rgba(11,140,11, 0.2)"
        }
    },

    {
        "id": "motorway",
        "type": "line",
        "source": "os",
        "source-layer": "motorway",
        "minzoom" : 6,
        "maxzoom" : 14,
         "paint": {
            "line-color": "rgba(11,11,11, 0.5)"
        }
    },

    {
        "id": "functionalsite",
        "type": "line",
        "source": "os",
        "source-layer": "functionalsite",
        "minzoom" : 6,
        "maxzoom" : 14,
         "paint": {
            "line-color": "rgba(100,11,11, 0.5)"
        }
    },


    // "carcharging" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_CarChargingPoint_WGS84.shp"],
    //     "minzoom" : 10,
    //     "maxzoom" : 14
    // },

    // "electricitylines" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_ElectricityTransmissionLine_WGS84.shp"],
    //     "minzoom" : 8,
    //     "maxzoom" : 14
    // },


    // "glasshouse" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_Glasshouse_WGS84.shp"],
    //     "minzoom" : 10,
    //     "maxzoom" : 14
    // },

    // "importantbuilding" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_ImportantBuilding_WGS84.shp"],
    //     "minzoom" : 10,
    //     "maxzoom" : 14
    // },
    
    // "railwaytrack" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_RailwayTrack_WGS84.shp"],
    //     "minzoom" : 8,
    //     "maxzoom" : 14
    // },

    // "railwaytunnel" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_RailwayTunnel_WGS84.shp"],
    //     "minzoom" : 8,
    //     "maxzoom" : 14
    // },

    // "railwaystation" : {
    //     "type" : "shapefile",
    //     "paths" : ["/tiler-data/input/os/TL_RailwayStation_WGS84.shp"],
    //     "minzoom" : 9,
    //     "maxzoom" : 14
    // }
]

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    zoom: 8,
    center: [-0.5, 51.0]
});

map.on('load', function () {
    console.log("Map ready to add vector tiles")
    map.addSource(vectortiles, {
        "type": "vector",
        "tiles": [url],
        // "maxzoom": 11,
        // "minzoom": 8
    });
    tilelayers.forEach(function(tiles){
        map.addLayer(tiles);
    })

});

map.addControl(new mapboxgl.NavigationControl());
