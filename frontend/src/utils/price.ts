type prettyPriceType = (price: number) => string;


const prettyPrice: prettyPriceType = (price) => {
    const parts = [];
    let currentPrice = price;
    while(currentPrice > 0){
        if (currentPrice < 1000){
            parts.unshift(currentPrice.toString());
            break;
        }
        const rest = currentPrice % 1000;
        parts.unshift(rest.toString().padEnd(3, '0'))
        currentPrice = Math.round(currentPrice / 1000);
    }
    return parts.join(" ");
}
export {prettyPrice};