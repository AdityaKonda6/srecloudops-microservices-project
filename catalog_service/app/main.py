from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from catalog_service.app.database import init_db, get_db
from catalog_service.app import models as db_models

app = FastAPI(title="Catalog Service")


class ProductCreate(BaseModel):
    id: str
    name: str
    price: float
    description: str


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    # Add sample products if empty
    db = next(get_db())
    if db.query(db_models.Product).count() == 0:
        sample_products = [
            db_models.Product(id="p1", name="Notebook", price=12.5, description="A simple paper notebook"),
            db_models.Product(id="p2", name="Keyboard", price=35.0, description="A mechanical-style keyboard"),
            db_models.Product(id="p3", name="Mouse", price=18.0, description="A wireless mouse"),
        ]
        db.add_all(sample_products)
        db.commit()
    db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    products = db.query(db_models.Product).all()
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)) -> ProductResponse:
    product = db.query(db_models.Product).filter(db_models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

