import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI(title="Microservices UI")

# Get service URLs from environment
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8001")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://localhost:8002")

# Setup templates
templates = Jinja2Templates(directory="ui/templates")


def fetch_products():
    """Fetch products from catalog service"""
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/products", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []


def fetch_orders():
    """Fetch orders from orders service"""
    try:
        response = requests.get(f"{ORDERS_SERVICE_URL}/orders", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []


def create_order(customer_name: str, product_id: str, product_name: str, unit_price: float, quantity: int):
    """Create an order via orders service"""
    try:
        payload = {
            "customer_name": customer_name,
            "product_id": product_id,
            "product_name": product_name,
            "unit_price": unit_price,
            "quantity": quantity,
        }
        response = requests.post(f"{ORDERS_SERVICE_URL}/orders", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to create order: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage - display products and order form"""
    products = fetch_products()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.post("/api/orders", response_class=HTMLResponse)
async def place_order(request: Request):
    """Handle order creation"""
    form_data = await request.form()
    customer_name = form_data.get("customer_name")
    product_id = form_data.get("product_id")
    quantity = int(form_data.get("quantity", 1))

    # Find product details
    products = fetch_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Product not found"})

    try:
        order = create_order(
            customer_name=customer_name,
            product_id=product["id"],
            product_name=product["name"],
            unit_price=product["price"],
            quantity=quantity,
        )
        return templates.TemplateResponse("order_success.html", {"request": request, "order": order})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    """Display all orders"""
    orders = fetch_orders()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "ui"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
