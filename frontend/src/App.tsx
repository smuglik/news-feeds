import {Product} from './components/product';
import {useEffect} from "react";
import ky from "ky";
import { IProduct } from './models';


function App() {
    // @ts-ignore
    const [products, setProducts] = useEffect([])

    async function requestProducts() {
        const data = await ky
            .get("https://fakestoreapi.com/products")
            .json()
        setProducts(data)

    }

    useEffect(() => {
        requestProducts()
    }, [])

    return (
        <div className='container mx-auto max-w-2xl pt-5'>
            {products.map((product: IProduct) => <Product product={product} key={product.id}/>)}
        </div>
    )
}

export default App;