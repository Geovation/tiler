var map = L.map('map');

L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    maxZoom: 8,
    minZoom: 3,
    noWrap: true  
}).addTo(this.map)


var Url = "/tiler/tiler-data/tiles/states/{z}/{x}/{y}.pbf";

var VectorTileOptions = {
    rendererFactory: L.canvas.tile,
    attribution: '',
   // vectorTileLayerStyles: vectorTileStyling
};


var PbfLayer = L.vectorGrid.protobuf(Url, VectorTileOptions).addTo(map);



map.setView({ lat: 37.2588581, lng:-104.646299 }, 1);
