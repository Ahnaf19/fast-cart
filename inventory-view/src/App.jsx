import { Products } from './components/products'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import { ProductsCreate } from './components/products_create'

function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<Products />} />
      <Route path="/create" element={<ProductsCreate />} />
    </Routes>
  </BrowserRouter>
}

export default App
