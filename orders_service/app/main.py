from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from orders_service.app.database import init_db, get_db
from orders_service.app import models as db_models

app = FastAPI(title="Orders Service")


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1)
    product_id: str = Field(min_length=1)
    product_name: str = Field(min_length=1)
    unit_price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: str
    customer_name: str
    product_id: str
    product_name: str
    unit_price: float
    quantity: int
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/orders", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)) -> list[OrderResponse]:
    orders = db.query(db_models.Order).order_by(db_models.Order.created_at.desc()).all()
    return orders


@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)) -> OrderResponse:
    total_amount = round(payload.unit_price * payload.quantity, 2)
    order = db_models.Order(
        id=str(uuid4()),
        customer_name=payload.customer_name,
        product_id=payload.product_id,
        product_name=payload.product_name,
        unit_price=payload.unit_price,
        quantity=payload.quantity,
        total_amount=total_amount,
        status="created",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

