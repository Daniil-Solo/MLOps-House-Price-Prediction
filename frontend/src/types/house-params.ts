interface HouseParams{
    latitude: number | null,
    longitude: number | null,
    houseType: string,
    houseFloor: number,
    elevatorCount: number,
    hasExtra: boolean,
    roomCount: number,
    area: number,
    apartmentFloor: number,
    repairType: string,
    terraceType: string,
    bathroomType: string,
    price: number | null
}

export type {HouseParams};