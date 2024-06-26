import React from "react";
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import Divider from '@mui/material/Divider';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import {HouseTypes, RepairTypes, TerraceTypes, BathroomTypes} from "./constants.ts";
import {HouseParams} from "../../types/house-params.ts";

interface HouseFormProps{
    params: HouseParams,
    setParams: (p: HouseParams) => void,
    predictPrice: () => void,
    priceLoading: boolean
}

const HouseForm: React.FC<HouseFormProps> = (props) => {
    const {params, setParams, predictPrice, priceLoading} = props;
    return (
        <Box
            component="form"
            sx={{ p: 2, backgroundColor: 'white', borderRadius: "8px" }}
            noValidate
            autoComplete="off"
        >
            <Stack direction="column" spacing={1}>
                <Typography variant="h6" gutterBottom>
                    Характеристики дома
                </Typography>
                <Stack direction="row" spacing={1}>
                    <FormControl size="small" fullWidth>
                        <InputLabel id="house-type-select-label">Тип дома</InputLabel>
                        <Select
                            labelId="house-type-select-label"
                            value={params.houseType}
                            onChange={e => setParams({...params, houseType: e.target.value})}
                            label="Тип дома"
                        >
                            {
                                HouseTypes.map(item => (
                                    <MenuItem key={item} value={item}>{item}</MenuItem>
                                ))
                            }
                        </Select>
                    </FormControl>
                    <TextField
                        fullWidth
                        label="Этажность дома"
                        type="number"
                        size="small"
                        value={params.houseFloor}
                        onChange={e=>setParams({...params, houseFloor: +e.target.value})}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                    <TextField
                        fullWidth
                        label="Число лифтов"
                        type="number"
                        size="small"
                        value={params.elevatorCount}
                        onChange={e=>setParams({...params, elevatorCount: +e.target.value})}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Stack>
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={params.hasExtra}
                            onChange={e=>setParams({...params, hasExtra: e.target.checked})}
                            color="success"
                            size={"small"}
                        />
                    }
                    label={
                        <Tooltip title="Консьерж, мусоропровод и т.п." placement="right">
                            <Typography variant="caption" display="block" fontSize="16px" mb={0} gutterBottom>
                                дополнительные услуги
                            </Typography>
                        </Tooltip>
                    }
                />

                <Typography variant="h6" gutterBottom>
                    Характеристики квартиры
                </Typography>
                <Stack direction="row" spacing={1}>
                    <TextField
                        fullWidth
                        label="Число комнат"
                        type="number"
                        size="small"
                        value={params.roomCount}
                        onChange={e=>setParams({...params, roomCount: +e.target.value})}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                    <TextField
                        fullWidth
                        label="Площадь в м²"
                        type="number"
                        size="small"
                        value={params.area}
                        onChange={e=>setParams({...params, area: +e.target.value})}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                    <TextField
                        fullWidth
                        label="Этаж квартиры"
                        type="number"
                        size="small"
                        value={params.apartmentFloor}
                        onChange={e=>setParams({...params, apartmentFloor: +e.target.value})}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />
                </Stack>
                <Stack direction="row" spacing={1}>
                    <FormControl size="small" fullWidth>
                        <InputLabel id="repair-type-select-label">Ремонт</InputLabel>
                        <Select
                            labelId="repair-type-select-label"
                            label="Ремонт"
                            value={params.repairType}
                            onChange={e => setParams({...params, repairType: e.target.value})}
                        >
                            {
                                RepairTypes.map(item => (
                                    <MenuItem key={item} value={item}>{item}</MenuItem>
                                ))
                            }
                        </Select>
                    </FormControl>
                    <FormControl size="small" fullWidth>
                        <InputLabel id="terrace-type-select-label">Балкон</InputLabel>
                        <Select
                            labelId="terrace-type-select-label"
                            label="Балкон"
                            value={params.terraceType}
                            onChange={e => setParams({...params, terraceType: e.target.value})}
                        >
                            {
                                TerraceTypes.map(item => (
                                    <MenuItem key={item} value={item}>{item}</MenuItem>
                                ))
                            }
                        </Select>
                    </FormControl>
                    <FormControl size="small" fullWidth>
                        <InputLabel id="bathroom-type-select-label">Санузел</InputLabel>
                        <Select
                            labelId="bathroom-type-select-label"
                            label="Санузел"
                            value={params.bathroomType}
                            onChange={e => setParams({...params, bathroomType: e.target.value})}
                        >
                            {
                                BathroomTypes.map(item => (
                                    <MenuItem key={item} value={item}>{item}</MenuItem>
                                ))
                            }
                        </Select>
                    </FormControl>
                </Stack>
                <Divider />
                <Button
                    disabled={params.latitude === null || params.longitude === null}
                    variant="contained"
                    size="small"
                    color="success"
                    onClick={predictPrice}
                >
                    Рассчитать стоимость
                </Button>
                <Typography variant="body1" gutterBottom>
                    {
                        params.latitude === null || params.longitude === null
                        ? "Требуется указать местоположение дома"
                        : priceLoading
                            ? "Цена рассчитывается ..."
                            : params.price === null
                                ? "Требуется пересчитать цену"
                                :`Рекомендуемая цена: ${Math.round(params.price)} руб.`
                    }
                </Typography>
            </Stack>
        </Box>
    )
}

export default HouseForm;