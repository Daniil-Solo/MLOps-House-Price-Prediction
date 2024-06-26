import {baseAxios} from "../axios.ts";
import {PredictionResult} from "../schemas/predict.ts";
import {HouseParams} from "../../types/house-params.ts";

const PREDICT_WITH_COORDINATES_URL = "/api/predict_with_coordinates";

const predictApartmentPrice = async (house: HouseParams): Promise<PredictionResult> => {
    const response = await baseAxios.post(
        PREDICT_WITH_COORDINATES_URL,
        {
            lat: house.latitude,
            lon: house.longitude,
            number_of_floors: house.houseFloor,
            type_of_house: house.houseType,
            number_of_rooms: house.roomCount,
            area_of_apartment: house.area,
            apartment_floor: house.apartmentFloor,
            repair: house.repairType,
            terrace: house.terraceType,
            extra: house.hasExtra,
            elevator: house.elevatorCount,
            bathroom: house.bathroomType,
        }
    );
    return response.data;
}

export {predictApartmentPrice};
