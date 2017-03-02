var map = L.map('map');

L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    maxZoom: 8,
    minZoom: 3,
    noWrap: true  
}).addTo(this.map)

var vectortiles = "UK"
var Url = "/tiler/tiler-data/tiles/" + vectortiles + "/{z}/{x}/{y}.pbf";

var vectorTileStyling = {
    "UKgeojson": function(properties, zoom) {
        console.log("Styling", properties, zoom)
        return  {
            fill: true,
            weight: 1,
            fillColor: '#06cccc',
            color: '#06cccc',
            fillOpacity: 0.2,
            opacity: 0.4,
        }
    }
}

var VectorTileOptions = {
    rendererFactory: L.canvas.tile,
    attribution: '',
    vectorTileLayerStyles: vectorTileStyling
};


var PbfLayer = L.vectorGrid.protobuf(Url, VectorTileOptions).addTo(map);


map.setView({ lat: 51.0, lng:0.1 }, 6);
