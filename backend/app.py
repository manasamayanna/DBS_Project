# Import required modules
from fastapi import FastAPI, Query, Path
from mySQLConnector import MySQLConnector
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()
app.debug = True

# Configure CORS (Cross-Origin Resource Sharing) middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the product data
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    image_url: str
    description: str
    category_id: int

# Create an instance of MySQLConnector
mysql = MySQLConnector()

# Route to get all products
@app.get("/products", response_model=list)
async def get_products(user_id: int = Query(..., description="User ID")):
    products = mysql.select_products(user_id)
    return products

# Route to get all categories
@app.get('/categories', response_model=list)
async def get_categories():
    categories = mysql.select_categories()
    return categories

# Route to create a product
@app.post("/products", response_model=str)
async def create_product(product: ProductBase, user_id: int = Query(..., description="User ID")):
    result = mysql.insert_product(user_id, product.name, product.price, product.stock, 
                                 product.image_url, product.description, product.category_id)
    return result

# Route to update a product
@app.put("/products/{product_id}", response_model=str)
async def update_product(product_id: int, product: ProductBase, user_id: int = Query(..., description="User ID")):
    result = mysql.update_product(user_id, product_id, product.name, product.price, product.stock, 
                                 product.image_url, product.description, product.category_id)
    return result

# Route to delete a product
@app.delete("/products/{product_id}", response_model=str)
async def delete_product(product_id: int, user_id: int = Query(..., description="User ID")):
    result = mysql.delete_product_by_id(user_id, product_id)
    return result

# Run the FastAPI app using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
