import {useState} from "react"
import {IProduct} from "../models"

interface ProductProps {
    product: IProduct
}

export function Product({product}: ProductProps) {
    return ProductHelper(product)
}

function renderButton(details: boolean, setDetails: any) {
    const buttonName = details ? "Hide details" : " Show details"
    return (
        <button
            className="py-2 px-4 border bg-yellow-400"
            onClick={() => setDetails(!details)}>
            {buttonName}
        </button>
    )
}

let getDescription = (details: boolean, description: string): JSX.Element => {
    if (details)
        return (<div>
            <p>{description}</p>
        </div>)
    else
        return (<div/>)
}


function ProductHelper(product: IProduct) {
    const [details, setDetails] = useState(false)
    return (
        <div className="border py-2 px-2 rounded flex flex-col items-center mb-2">
            <img src={product.image} className="w-1/6" alt={product.title}/>
            {renderButton(details, setDetails)}
            {getDescription(details, product.description)}
        </div>
    )
}