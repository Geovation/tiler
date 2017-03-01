/* eslint-disable openlayers-internal/no-unused-requires */

var extent =  [-178.217598, 18.921786, -66.969271, 71.406235] //geojsonSource.getExtent();

var proj = new ol.proj.Projection({
    code: 'EPSG:4326',
    units: 'm',
    extent: [-180.0000, -90.0000, 180.0000, 90.0000]
});

var map = new ol.Map({
    layers: [
        new ol.layer.VectorTile({
            source: new ol.source.VectorTile({
                //   attributions: '',
                renderMode: 'vector',
                format: new ol.format.MVT(),
                tileGrid: ol.tilegrid.createXYZ({
                    maxZoom: 10,
                    extent: extent
                }),
                extent: extent,
                //   tilePixelRatio: 16,
                url: '/tiler/tiler-data/tiles/states/{z}/{x}/{y}.pbf'
                }),
                style: createStyle()
        }),
        new ol.layer.Tile({
            source: new ol.source.OSM(),
            opacity: 0.3
        })
    ],
    extent: extent,
    target: 'map',
    view: new ol.View({
        center: [-104.646299, 37.2588581],
        projection: proj,
        zoom: 6,
        minZoom: 1
    })
});


function createStyle () {

var color = 'rgba(255,0,0,0.5)';
var fill = new ol.style.Fill({color: color});
var stroke = new ol.style.Stroke({color: color, width: 1});

var polygon = new ol.style.Style({fill: fill});
var strokedPolygon = new ol.style.Style({fill: fill, stroke: stroke});
var line = new ol.style.Style({stroke: stroke});
var text = new ol.style.Style({text: new ol.style.Text({
text: 'Hello', fill: fill, stroke: stroke
})});

var styles = [polygon, strokedPolygon, line];
return polygon;
}

// ol.style.Fill, ol.style.Icon, ol.style.Stroke, ol.style.Style and
// ol.style.Text are required for createMapboxStreetsV6Style()