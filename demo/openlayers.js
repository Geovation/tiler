/* eslint-disable openlayers-internal/no-unused-requires */

var map = new ol.Map({
    layers: [
        new ol.layer.VectorTile({
            source: new ol.source.VectorTile({
                //   attributions: '',
                renderMode: 'vector',
                format: new ol.format.MVT(),
                tileGrid: ol.tilegrid.createXYZ({
                    maxZoom: 9,
                    // extent: extent
                }),
                // extent: extent,
                tilePixelRatio: 16,
                url: '/tiler/tiler-data/tiles/'+vectortiles+'/{z}/{x}/{y}.pbf'
            }),
            style: createStyle()
        }),
        new ol.layer.Tile({
            source: new ol.source.OSM(),
            opacity: 0.3
        })
    ],
    target: 'map',
    view: new ol.View({
        center: ol.proj.transform([0, 0], 'EPSG:4326','EPSG:3857'),
        zoom: 3,
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
    return styles;
}

// ol.style.Fill, ol.style.Icon, ol.style.Stroke, ol.style.Style and
// ol.style.Text are required for createMapboxStreetsV6Style()