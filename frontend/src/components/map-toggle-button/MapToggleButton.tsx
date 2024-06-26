import React from "react";
import './MapToggleButton.css';

interface MapToggleButtonProps{
    isActive: boolean,
    onClick: () => void,
    image: string,
    hint_message: string
}

const MapToggleButton: React.FC<MapToggleButtonProps> = (props) => {

    return (
        <button
            className={props.isActive? "map-toggle-btn map-toggle-btn_active": "map-toggle-btn"}
            onClick={props.onClick} title={props.hint_message}
        >
            <img
                className="map-toggle-btn__image"
                src={props.image} alt="Картинка кнопки"
            />
        </button>
    )
}

export default MapToggleButton;