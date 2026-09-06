
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    discount_price: Optional[float] = None
    quantity: int = Field(ge=0)
    category: str
    sku: str = Field(min_length=5, max_length=20)
    email: EmailStr
    stock: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, value):
        return value.strip()

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value):
        value = value.upper()

        if " " in value:
            raise ValueError("SKU must not contain spaces")

        return value

    @model_validator(mode="after")
    def validate_discount_price(self):
        if self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValueError("discount_price must be less than price")

        return self


class ProductResponse(BaseModel):
    name: str
    price: float
    discount_price: Optional[float] = None
    quantity: int
    category: str
    stock: bool


products = []


@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


@app.post("/products", response_model=ProductResponse)
def create_product(product: Product):
    products.append(product)
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: Product):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")

    products[product_id] = product
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id < 0 or product_id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")

    products.pop(product_id)

    return {"message": "Product deleted successfully"}

