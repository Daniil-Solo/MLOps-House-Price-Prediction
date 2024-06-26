interface DistrictPopup{
    longitude: number,
    latitude: number,
    name: string
}

interface ApartmentInfo{
    apartment: string,
    price: number
}

interface ApartmentPopup{
    longitude: number,
    latitude: number,
    house: string,
    apartments: Array<ApartmentInfo>

}


export type {DistrictPopup, ApartmentPopup, ApartmentInfo};