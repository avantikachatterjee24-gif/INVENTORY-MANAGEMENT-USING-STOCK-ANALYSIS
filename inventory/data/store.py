from __future__ import annotations

from datetime import datetime

PRODUCTS = [
    {"id": 1, "name": "Product A", "stock": 50, "price": 29.99, "expiry_date": "2026-03-30"},
    {"id": 2, "name": "Product B", "stock": 30, "price": 19.99, "expiry_date": "2026-03-25"},
]

SALES_DATA = [
    {
        "id": 1,
        "product_id": 1,
        "product_name": "Product A",
        "qty": 5,
        "total": 149.95,
        "timestamp": "2024-10-15 10:30",
    },
    {
        "id": 2,
        "product_id": 2,
        "product_name": "Product B",
        "qty": 3,
        "total": 59.97,
        "timestamp": "2024-10-16 14:20",
    },
]


def append_sale(product_id: int, product_name: str, qty: int, unit_price: float) -> None:
    sale_total = qty * unit_price
    SALES_DATA.append(
        {
            "id": len(SALES_DATA) + 1,
            "product_id": product_id,
            "product_name": product_name,
            "qty": qty,
            "total": round(sale_total, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )


def add_product(name: str, stock: int, price: float, expiry_date: str = "2026-12-31") -> None:
    PRODUCTS.append(
        {
            "id": len(PRODUCTS) + 1,
            "name": name,
            "stock": stock,
            "price": price,
            "expiry_date": expiry_date,
        }
    )


def update_product(pid: int, name: str, stock: int, price: float) -> bool:
    for item in PRODUCTS:
        if item["id"] == pid:
            item["name"] = name
            item["stock"] = stock
            item["price"] = price
            return True
    return False


def delete_product(pid: int) -> None:
    PRODUCTS[:] = [item for item in PRODUCTS if item["id"] != pid]
