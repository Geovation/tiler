
var vectortiles = "buildings_wgs84";
var layername = vectortiles + "geojson";
var PORT = "8080";
var HOST = "http://127.0.0.1";
var url = HOST + ":"+ PORT + "/tiler/tiler-data/tiles/" + vectortiles + "/{z}/{x}/{y}.pbf";
console.log(url);

mapboxgl.accessToken = 'pk.eyJ1IjoiamFtZXNtaWxuZXIiLCJhIjoiY2lsMm96djd1MDBjYndnbTVmajAxeHByaiJ9.mw4lltZ8qZjJHaJwbnN5Yw';

var tiles = {
    "id": layername,
    "type": "fill",
    "source": vectortiles,
    "source-layer": layername,
    "filter": ["==", "$type", "Polygon"],
    "paint": {
        "fill-color": "rgba(255,11,11, 0.5)",
        // "line-color": "rgba(0,0,0, 0.1)"
    }
}

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
    map.addLayer(tiles);
});

map.addControl(new mapboxgl.NavigationControl());
