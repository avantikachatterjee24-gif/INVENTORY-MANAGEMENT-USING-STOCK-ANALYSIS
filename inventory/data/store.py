from __future__ import annotations

from datetime import datetime

PRODUCTS = [
    {
        "id": 1,
        "name": "Product A",
        "stock": 120,
        "price": 29.99,
        "cost_price": 18.0,
        "expiry_date": "2026-03-30",
    },
    {
        "id": 2,
        "name": "Product B",
        "stock": 10,
        "price": 19.99,
        "cost_price": 12.0,
        "expiry_date": "2026-03-25",
    },
    {
        "id": 3,
        "name": "Product C",
        "stock": 0,
        "price": 39.99,
        "cost_price": 24.0,
        "expiry_date": "2026-06-15",
    },
]

SALES_DATA = [
    # Product A sales — spread over multiple days
    {"id": 1,  "product_id": 1, "product_name": "Product A", "qty": 5,  "total": 149.95, "timestamp": "2024-10-01 09:00"},
    {"id": 2,  "product_id": 1, "product_name": "Product A", "qty": 8,  "total": 239.92, "timestamp": "2024-10-05 11:00"},
    {"id": 3,  "product_id": 1, "product_name": "Product A", "qty": 6,  "total": 179.94, "timestamp": "2024-10-10 14:00"},
    {"id": 4,  "product_id": 1, "product_name": "Product A", "qty": 10, "total": 299.90, "timestamp": "2024-10-15 10:30"},
    {"id": 5,  "product_id": 1, "product_name": "Product A", "qty": 9,  "total": 269.91, "timestamp": "2024-10-20 16:00"},
    {"id": 6,  "product_id": 1, "product_name": "Product A", "qty": 12, "total": 359.88, "timestamp": "2024-10-25 09:45"},
    {"id": 7,  "product_id": 1, "product_name": "Product A", "qty": 11, "total": 329.89, "timestamp": "2024-10-30 13:00"},

    # Product B sales — spread over multiple days
    {"id": 8,  "product_id": 2, "product_name": "Product B", "qty": 3,  "total": 59.97,  "timestamp": "2024-10-02 10:00"},
    {"id": 9,  "product_id": 2, "product_name": "Product B", "qty": 5,  "total": 99.95,  "timestamp": "2024-10-08 12:00"},
    {"id": 10, "product_id": 2, "product_name": "Product B", "qty": 4,  "total": 79.96,  "timestamp": "2024-10-14 15:00"},
    {"id": 11, "product_id": 2, "product_name": "Product B", "qty": 7,  "total": 139.93, "timestamp": "2024-10-20 11:30"},
    {"id": 12, "product_id": 2, "product_name": "Product B", "qty": 6,  "total": 119.94, "timestamp": "2024-10-26 09:00"},

    # Product C sales — spread over multiple days
    {"id": 13, "product_id": 3, "product_name": "Product C", "qty": 2,  "total": 79.98,  "timestamp": "2024-10-03 08:30"},
    {"id": 14, "product_id": 3, "product_name": "Product C", "qty": 4,  "total": 159.96, "timestamp": "2024-10-12 10:00"},
    {"id": 15, "product_id": 3, "product_name": "Product C", "qty": 3,  "total": 119.97, "timestamp": "2024-10-18 14:30"},
    {"id": 16, "product_id": 3, "product_name": "Product C", "qty": 5,  "total": 199.95, "timestamp": "2024-10-24 16:00"},
    {"id": 17, "product_id": 3, "product_name": "Product C", "qty": 6,  "total": 239.94, "timestamp": "2024-10-29 11:00"},
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


def add_product(
    name: str,
    stock: int,
    price: float,
    cost_price: float | None = None,
    expiry_date: str = "2026-12-31",
) -> None:
    resolved_cost = cost_price if cost_price is not None else round(price * 0.6, 2)
    PRODUCTS.append(
        {
            "id": len(PRODUCTS) + 1,
            "name": name,
            "stock": stock,
            "price": price,
            "cost_price": resolved_cost,
            "expiry_date": expiry_date,
        }
    )


def update_product(pid: int, name: str, stock: int, price: float, cost_price: float | None = None) -> bool:
    for item in PRODUCTS:
        if item["id"] == pid:
            item["name"] = name
            item["stock"] = stock
            item["price"] = price
            item["cost_price"] = cost_price if cost_price is not None else item.get("cost_price", round(price * 0.6, 2))
            return True
    return False


def delete_product(pid: int) -> None:
    PRODUCTS[:] = [item for item in PRODUCTS if item["id"] != pid]
