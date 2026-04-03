from __future__ import annotations

from datetime import datetime

from inventory.data.store import PRODUCTS, SALES_DATA
from inventory.ml.demand_model import predict_demand



def sales_stats() -> dict:
    return {
        "total_sales": sum(int(item.get("qty", 0)) for item in SALES_DATA),
        "total_revenue": sum(float(item.get("total", 0.0)) for item in SALES_DATA),
    }



def product_days_left() -> dict[int, int]:
    days_left: dict[int, int] = {}
    for product in PRODUCTS:
        expiry = datetime.strptime(product["expiry_date"], "%Y-%m-%d")
        diff = (expiry - datetime.now()).days
        days_left[product["id"]] = diff
    return days_left



def dashboard_payload() -> dict:
    return {
        "total_products": len(PRODUCTS),
        "total_sales_qty": sum(int(item.get("qty", 0)) for item in SALES_DATA),
        "total_revenue": sum(float(item.get("total", 0.0)) for item in SALES_DATA),
        "fastest_product": PRODUCTS[0]["name"] if PRODUCTS else "N/A",
        "dead_stock": len([p for p in PRODUCTS if int(p.get("stock", 0)) == 0]),
        "ml_predicted_demand": predict_demand(SALES_DATA),
        "insights": ["System running smoothly"],
        "ml_comparison": [{"day": "Day 1", "actual": 5, "predicted": 6}],
        "chart_url": "",
    }
