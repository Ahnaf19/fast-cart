// import { useEffect } from "react"
import { useEffect, useState } from "react"
import { Wrapper } from "./wrapper"
import {Link} from "react-router-dom"

export const Products = () => {
    const [products, setProducts] = useState([])
    useEffect(() => {
      (async () => {
        const response = await fetch('http://localhost:8000/inventory/products')
        const content = await response.json()
        console.log("Fetched Products:", content)
        setProducts(content)
      }) ()
    }, [])

    const del = async id => {
      if(window.confirm("Are you sure to delete this record?")) {
          await fetch(`http://localhost:8000/inventory/product/${id}`, {
            method: 'DELETE'
          })
          setProducts(products.filter(product => product.id !== id))
      }
    }

    return  <Wrapper>
              <div style={{marginTop: "20px"}}>
                <Link to={`/create`} className="btn btn-sm btn-outline-success">Add</Link>
              </div>
              <div className="table-responsive small mt-4">
                <table className="table table-striped table-sm">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Product Name</th>
                      <th scope="col">Unit Price</th>
                      <th scope="col">Quantity</th>
                      <th scope="col">Creation Time</th>
                      <th scope="col">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {products.map(product => {
                      return <tr key={product.id}>
                      <td>{product.id}</td>
                      <td>{product.name}</td>
                      <td>{product.price}</td>
                      <td>{product.quantity}</td>
                      <td>{new Date(product.creation_time).toLocaleString('en-US', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true
                      })}</td>
                      <td>
                        <button type="button" className="btn btn-sm btn-outline-danger"
                          onClick={() => del(product.id)}
                        >
                          Delete</button>
                      </td>
                    </tr>
                    })}
                  </tbody>
                </table>
              </div>
        </Wrapper>
}
