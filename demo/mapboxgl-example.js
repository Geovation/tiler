
// var vectortiles = "buildings_wgs84";
var layername = vectortiles;
var PORT = "8080";
var HOST = "http://127.0.0.1";
var url = HOST + ":"+ PORT + "/tiler/tiler-data/tiles/" + vectortiles + "/{z}/{x}/{y}.pbf";
console.log(url);

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNtaWxuZXIiLCJhIjoiY2lsMm96djd1MDBjYndnbTVmajAxeHByaiJ9.mw4lltZ8qZjJHaJwbnN5Yw';

var tilelayers = [
    {
        "id": layername,
        "type": "fill",
        "source": vectortiles,
        "source-layer": layername,
        "filter": ["==", "$type", "Polygon"],
        "paint": {
            "fill-color": "rgba(255,11,11, 0.5)"
        }
    },
    {
        "id": "stations",
        "type": "circle",
        "source": vectortiles,
        "source-layer": "stations",
        "filter": ["==", "$type", "Point"],
         'circle-radius': {
                'base': 1.75,
                'stops': [[12, 2], [22, 180]]
        },
        // color circles by ethnicity, using data-driven styles
        // 'circle-color': {
        //     stops: [
        //         ['White', '#fbb03b'],
        //         ['Black', '#223b53'],
        //         ['Hispanic', '#e55e5e'],
        //         ['Asian', '#3bb2d0'],
        //         ['Other', '#ccc']]
        // }
    }

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
