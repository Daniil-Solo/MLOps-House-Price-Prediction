import {apartmentsDataPath, apartmentsSourceId, districtsDataPath, districtsSourceId} from "./constants.ts";
import {SourceSpecification} from "maplibre-gl";


type sourceSpec = () => [string, SourceSpecification];

const createDistrictsSourceSpec: sourceSpec = () => {
    return  [
        districtsSourceId,
        {
            type: "geojson",
            data: districtsDataPath,
        }
    ]
}

const createApartmentsSourceSpec: sourceSpec = () => {
    return  [
        apartmentsSourceId,
        {
            type: "geojson",
            data: apartmentsDataPath,
        }
    ]
}


export {createDistrictsSourceSpec, createApartmentsSourceSpec};