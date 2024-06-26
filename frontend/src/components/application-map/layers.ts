import {
    districtsColorOpacity,
    districtsLayerId,
    districtsSourceId,
    districtColorField,
    apartmentsLayerId,
    apartmentsSourceId,
    apartmentsPriceField, apartmentsHeatmapLayerId
} from "./constants.ts";
import {AddLayerObject} from "maplibre-gl";


type layerSpec = (visibility: "visible" | "none") => AddLayerObject;

const createDistrictsLayerSpec: layerSpec = (visibility)  => {
    return  {
        id: districtsLayerId,
        source: districtsSourceId,
        type: "fill-extrusion",
        layout: {
            visibility: visibility
        },
        "paint": {
            'fill-extrusion-color': ["get", districtColorField],
            'fill-extrusion-height': 1,
            'fill-extrusion-opacity': districtsColorOpacity,
        }
    }
}

const createApartmentsHeatmapLayerSpec: layerSpec = (visibility)  => {
    return  {
        id: apartmentsHeatmapLayerId,
        source: apartmentsSourceId,
        type: 'heatmap',
        maxzoom: 14,
        layout: {
            visibility: visibility
        },
        "paint": {
            'heatmap-weight': [
                'interpolate',
                ['linear'],
                ['get', apartmentsPriceField],
                800000,
                0,
                20000000,
                1
            ],
            'heatmap-intensity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                1,
                14,
                5
            ],
            'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0,
                'rgba(33,102,172,0)',
                0.2,
                'rgb(103,169,207)',
                0.4,
                'rgb(209,229,240)',
                0.6,
                'rgb(253,219,199)',
                0.8,
                'rgb(239,138,98)',
                1,
                'rgb(178,24,43)'
            ],
            'heatmap-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                2,
                14,
                15
            ],
            'heatmap-opacity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                12,
                1,
                14,
                0
            ]
        }
    }
}

const createApartmentsLayerSpec: layerSpec = (visibility)  => {
    return  {
        id: apartmentsLayerId,
        source: apartmentsSourceId,
        type: 'circle',
        minzoom: 14,
        layout: {
            visibility: visibility
        },
        "paint": {
            'circle-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                14,
                4,
                20,
                30
            ],
            'circle-color': [
                'interpolate',
                ['linear'],
                ['get', apartmentsPriceField],
                800000,
                'rgba(33,102,172,0)',
                1500000,
                'rgb(103,169,207)',
                3000000,
                'rgb(209,229,240)',
                5000000,
                'rgb(253,219,199)',
                10000000,
                'rgb(239,138,98)',
                20000000,
                'rgb(178,24,43)'
            ],
            'circle-stroke-color': 'black',
            'circle-stroke-width': 1,
            'circle-opacity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                13,
                0,
                14,
                1
            ]
        }
    }
}


export {createDistrictsLayerSpec, createApartmentsHeatmapLayerSpec, createApartmentsLayerSpec};