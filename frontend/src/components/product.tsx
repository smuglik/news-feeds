import { useState } from "react"
import { IProduct } from "../models"

interface ProductProps{
    product: IProduct
}
export function Product({product}: ProductProps) {
    const [details, setDetails] = useState(false)
    return (
        <div className="border py-2 px-2 rounded flex flex-col items-center mb-2">
            <img src={product.image} className="w-1/6" alt={product.title}/>
            <button></button>
        </div>
    )
}