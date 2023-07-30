import { createElement as e, useState } from 'react';
import { Product } from './components/product';
import { products } from './data/products';

function App() {
  return (
    <div className='container mx-auto max-w-2xl pt-5'>
      <Product product={products[0]} />
      <Product product={products[1]} />
    </div>
  )
}

export default App;
