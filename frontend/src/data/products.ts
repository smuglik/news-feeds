import ky from "ky";
import {IProduct} from "../models";

// @ts-ignore
export async function requestProducts(): Promise<IProduct[]> {
    try{
        return <IProduct[]>await ky
            .get("https://fakestoreapi.com/products")
            .json()
    } catch (e) {
        console.log(e)
    }
}
