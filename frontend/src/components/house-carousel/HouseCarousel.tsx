import React from "react";
import {ApartmentInfo} from "../../types/popup.ts";
import CircleIcon from '@mui/icons-material/Circle';
import {prettyPrice} from "../../utils/price.ts";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";

interface HouseCarouselProps{
    house: string,
    apartments: Array<ApartmentInfo>
}

const HouseCarousel: React.FC<HouseCarouselProps> = (props) => {
    const {house, apartments} = props;
    const [currentIndex, setCurrentIndex] = React.useState(0);
    return (
        <Box
            component="div"
        >
            <Stack direction="column" spacing={1}>
                <Typography variant="body1" gutterBottom>
                    {house}
                </Typography>
                <Divider />
                <Typography variant="body2" gutterBottom minHeight={104}>
                    {apartments[currentIndex].apartment}
                    <br/>
                    Цена: {prettyPrice(apartments[currentIndex].price)} руб.
                </Typography>
                <Divider />
                <div style={{display: "flex", alignItems: "center", justifyContent: "center", overflowX: "auto"}}>
                {
                    apartments.map(
                        (_, index) => (
                            <CircleIcon
                                key={index}
                                fontSize={"small"}
                                htmlColor={currentIndex === index? "#494949": "grey"}
                                onClick={() => setCurrentIndex(index)}
                                style={{cursor: "pointer"}}
                            />
                        )
                    )
                }
                </div>
            </Stack>
        </Box>
    )
}

export default HouseCarousel;