import Map, { MapRef, Marker, MapLayerMouseEvent, FullscreenControl, NavigationControl, Popup} from 'react-map-gl/maplibre';
import {Dispatch, SetStateAction, useRef, useState} from "react";
import MapToggleButton from "../map-toggle-button/MapToggleButton.tsx";
import logoHexagon from './../../assets/hexagon.svg';
import logoHouse from './../../assets/house.svg';
import logoParams from './../../assets/params.svg';
import logoBars from './../../assets/bars.svg';
import {createApartmentsSourceSpec, createDistrictsSourceSpec} from "./sources.ts";
import {createApartmentsHeatmapLayerSpec, createApartmentsLayerSpec, createDistrictsLayerSpec} from "./layers.ts";
import {
    apartmentsApartmentField, apartmentsHeatmapLayerId,
    apartmentsHouseField,
    apartmentsLayerId, apartmentsPriceField,
    districtNameField,
    districtsLayerId
} from "./constants.ts";
import {ApartmentPopup, DistrictPopup} from "../../types/popup.ts";
import {OwnHouse} from "../../types/own-house.ts";
import {MapView} from "../../types/mapview.ts";
import "./ApplicationMap.css";
import HouseForm from "../house-form/HouseForm.tsx";
import {HouseParams} from "../../types/house-params.ts";
import {BathroomTypes, HouseTypes, RepairTypes, TerraceTypes} from "../house-form/constants.ts";
import {predictApartmentPrice} from "../../api/router/predict.ts";
import {toast} from "react-toastify";
import HouseCarousel from "../house-carousel/HouseCarousel.tsx";
const BASE_MAP_URL = import.meta.env.VITE_BASE_MAP_URL || "";


// city Perm
const initialMapView: MapView = {
    longitude: 56.2502,
    latitude: 58.0105,
    zoom: 12,
    pitch: 0
}

const initialHouseParams: HouseParams = {
    latitude: null,
    longitude: null,
    houseType: HouseTypes[0],
    houseFloor: 9,
    elevatorCount: 2,
    hasExtra: false,
    roomCount: 1,
    area: 40,
    apartmentFloor: 3,
    repairType: RepairTypes[0],
    terraceType: TerraceTypes[0],
    bathroomType: BathroomTypes[0],
    price: null
}


const ApplicationMap = () => {
    const mapRef = useRef<MapRef>(null);
    const [mapview, setMapview] = useState<MapView>(initialMapView);
    const [visibleDistricts, setVisibleDistricts] = useState(false);
    const [visibleApartments, setVisibleApartments] = useState(false);
    const [visibleParameters, setVisibleParameters] = useState(false);
    const [selectMarker, setSelectMarker] = useState(false);
    const [ownHouse, setOwnHouse] = useState<OwnHouse | null>(null)
    const [districtPopup, setDistrictPopup] = useState<DistrictPopup | null>(null);
    const [apartmentPopup, setApartmentPopup] = useState<ApartmentPopup | null>(null);
    const [houseParams, setHouseParams] = useState<HouseParams>(initialHouseParams);
    const [loading, setLoading] = useState(false);
    const getMap = () => {
        if (mapRef.current === undefined || mapRef.current === null)
            throw Error("No current map");
        return mapRef.current.getMap();
    }

    const handleClick = (e:  MapLayerMouseEvent) => {
        if (selectMarker){
            const { lat, lng} = e.lngLat;
            setOwnHouse({latitude: lat, longitude: lng});
            setHouseParams({...houseParams, latitude: lat, longitude: lng})
            setSelectMarker(false);
        }
    }
    const toggleLayerView = (isVisibleLayer: boolean, layerIdList: Array<string>, setVisibleLayer: Dispatch<SetStateAction<boolean>>) => {
        const map = getMap();
        const visibility = isVisibleLayer? "none": "visible";
        layerIdList.forEach(layerId => {
            map.setLayoutProperty(layerId, "visibility", visibility);
        })
        setVisibleLayer(!isVisibleLayer);
    }

    const addSourcesAndLayers = () => {
        const map = getMap();
        const districtsLayerVisibility = visibleDistricts? "visible": "none";
        const apartmentsLayerVisibility = visibleApartments? "visible": "none";
        map.addSource(...createDistrictsSourceSpec());
        map.addLayer(createDistrictsLayerSpec(districtsLayerVisibility));
        map.addSource(...createApartmentsSourceSpec());
        map.addLayer(createApartmentsHeatmapLayerSpec(apartmentsLayerVisibility));
        map.addLayer(createApartmentsLayerSpec(apartmentsLayerVisibility));
        map.on('contextmenu', districtsLayerId, (e) => {
            if (e.features == undefined){
                return
            }
            const districtPopupData: DistrictPopup = {
                longitude: e.lngLat.lng,
                latitude: e.lngLat.lat,
                name: e.features[0].properties[districtNameField],
            }
            setDistrictPopup(districtPopupData)
        });
        map.on('click', apartmentsLayerId, (e) => {
            if (e.features == undefined){
                return
            }
            const apartmentPopupData: ApartmentPopup = {
                longitude: e.lngLat.lng,
                latitude: e.lngLat.lat,
                house: e.features[0].properties[apartmentsHouseField],
                apartments: e.features.map(f => ({apartment: f.properties[apartmentsApartmentField], price: f.properties[apartmentsPriceField]}))
            }
            setApartmentPopup(apartmentPopupData);
        });
    }

    const setParamsWithNullPrice = (params: HouseParams) => {
        if (params.area < 1 || params.elevatorCount < 0 || params.roomCount < 1 || params.apartmentFloor < 1 || params.houseFloor < 1)
            return;
        if (params.area > 200 || params.elevatorCount > 20 || params.roomCount > 12 || params.apartmentFloor > 30 || params.houseFloor > 30)
            return;
        if (params.apartmentFloor > params.houseFloor)
            return;
        setHouseParams({...params, price: null});
    }


    const predictPrice = () => {
        setLoading(true);
        setHouseParams({...houseParams, price: null});
        predictApartmentPrice(houseParams)
        .then(res =>{
            setHouseParams({...houseParams, price: res.value});
        })
        .catch(reason => {
            let message = undefined;
            if (reason?.response === undefined){
                message = "Сервис прогноза недоступен"
            } else if (reason?.response?.status === 400){
                message = reason?.response?.data?.message
            } else if (reason?.response?.status === 422){
                message = "Проверьте данные на корректность"
            }
            if (message === undefined){
                message = "Возникла ошибка. Повторите расчет позже";
            }
            toast.error(message)
            console.log(reason)
        })
        .finally(() => setLoading(false))
    }

    return (
        <Map
            longitude={mapview.longitude}
            latitude={mapview.latitude}
            zoom={mapview.zoom}
            pitch={mapview.pitch}
            style={{height: "100%", width: "100%"}}
            onMove={(e) => setMapview({longitude: e.viewState.longitude, latitude: e.viewState.latitude,zoom: e.viewState.zoom, pitch: e.viewState.pitch})}
            mapStyle={BASE_MAP_URL}
            ref={mapRef}
            onLoad={addSourcesAndLayers}
            onClick={handleClick}
        >
            <FullscreenControl/>
            <NavigationControl/>
            <div className="map__buttons">
                <MapToggleButton
                    isActive={visibleDistricts}
                    image={logoHexagon}
                    hint_message={"Отобразить/скрыть районы города"}
                    onClick={() => toggleLayerView(visibleDistricts, [districtsLayerId], setVisibleDistricts)}
                />
                <MapToggleButton
                    isActive={selectMarker}
                    image={logoHouse}
                    hint_message={"Выбрать дом"}
                    onClick={() => setSelectMarker(true)}
                />
                <MapToggleButton
                    isActive={visibleParameters}
                    image={logoParams}
                    hint_message={"Отобразить/скрыть параметры квартиры"}
                    onClick={() => setVisibleParameters(!visibleParameters)}
                />
            </div>
            <div className="map__buttons-2">
                <MapToggleButton
                    isActive={visibleApartments}
                    image={logoBars}
                    hint_message={"Отобразить/скрыть квартиры"}
                    onClick={() => toggleLayerView(visibleApartments, [apartmentsHeatmapLayerId, apartmentsLayerId], setVisibleApartments)}
                />
            </div>
            {
                districtPopup && (
                    <Popup
                        longitude={districtPopup.longitude}
                        latitude={districtPopup.latitude}
                        anchor="bottom"
                        onClose={() => setDistrictPopup(null)}
                        closeButton={false}
                    >
                        {districtPopup.name}
                    </Popup>
                )
            }
            {
                ownHouse && (
                    <Marker
                        longitude={ownHouse.longitude}
                        latitude={ownHouse.latitude}
                        anchor="bottom"
                    >
                        <img src={logoHouse} alt="Новый магазин"/>
                    </Marker>
                )
            }
            {
                visibleParameters && (
                    <div className="map__house-form">
                        <HouseForm
                            params={houseParams}
                            setParams={setParamsWithNullPrice}
                            predictPrice={predictPrice}
                            priceLoading={loading}
                        />
                    </div>
                )
            }
            {
                apartmentPopup && (
                    <Popup
                        longitude={apartmentPopup.longitude}
                        latitude={apartmentPopup.latitude}
                        anchor="top"
                        onClose={() => setApartmentPopup(null)}
                        closeButton={false}
                    >
                        <HouseCarousel
                            house={apartmentPopup.house}
                            apartments={apartmentPopup.apartments}
                        />
                    </Popup>
                )
            }
        </Map>
    )
}

export default ApplicationMap;