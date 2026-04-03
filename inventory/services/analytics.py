from __future__ import annotations

import base64
from collections import defaultdict
from datetime import datetime
from io import BytesIO

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from inventory.data.store import PRODUCTS, SALES_DATA
from inventory.ml.demand_model import predict_demand, predict_all_products, train_and_predict



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


def stock_status_report() -> list[dict]:
    report: list[dict] = []
    for item in PRODUCTS:
        stock = int(item.get("stock", 0))
        if stock <= 0:
            status = "Out of Stock"
            symbol = "❌"
            badge = "danger"
        elif stock <= 10:
            status = "Low Stock"
            symbol = "⚠️"
            badge = "warning"
        else:
            status = "Available"
            symbol = "✅"
            badge = "success"

        report.append(
            {
                "id": item["id"],
                "name": item["name"],
                "stock": stock,
                "status": status,
                "symbol": symbol,
                "badge": badge,
            }
        )
    return report


def profit_loss_analysis() -> dict:
    product_map = {p["id"]: p for p in PRODUCTS}
    total_sales = 0.0
    total_cost = 0.0

    for sale in SALES_DATA:
        qty = int(sale.get("qty", 0))
        revenue = float(sale.get("total", 0.0))
        total_sales += revenue

        product = product_map.get(int(sale.get("product_id", -1)))
        if product:
            cost_price = float(product.get("cost_price", round(float(product.get("price", 0.0)) * 0.6, 2)))
            total_cost += cost_price * qty
        else:
            total_cost += revenue * 0.65

    profit = total_sales - total_cost
    return {
        "total_sales": round(total_sales, 2),
        "total_cost": round(total_cost, 2),
        "profit": round(profit, 2),
        "status": "Profit" if profit >= 0 else "Loss",
    }


def _figure_to_base64() -> str:
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def stock_bar_chart() -> str:
    names = [item["name"] for item in PRODUCTS]
    stocks = [int(item.get("stock", 0)) for item in PRODUCTS]
    colors = ["#22c55e" if s > 10 else "#f59e0b" if s > 0 else "#ef4444" for s in stocks]

    plt.figure(figsize=(7, 4))
    plt.bar(names, stocks, color=colors)
    plt.title("Stock Levels by Product")
    plt.xlabel("Products")
    plt.ylabel("Units")
    return _figure_to_base64()


def sales_line_chart() -> str:
    daily_sales: dict[str, float] = defaultdict(float)
    for sale in SALES_DATA:
        timestamp = str(sale.get("timestamp", ""))
        day = timestamp.split(" ")[0] if timestamp else "Unknown"
        daily_sales[day] += float(sale.get("total", 0.0))

    labels = sorted(daily_sales.keys())
    values = [round(daily_sales[day], 2) for day in labels]

    plt.figure(figsize=(7, 4))
    plt.plot(labels, values, marker="o", linewidth=2.5, color="#2563eb")
    plt.title("Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue (INR)")
    plt.grid(alpha=0.25)
    return _figure_to_base64()


def stock_pie_chart() -> str:
    names = [item["name"] for item in PRODUCTS]
    stocks = [max(0, int(item.get("stock", 0))) for item in PRODUCTS]
    if sum(stocks) == 0:
        names = ["No Stock"]
        stocks = [1]

    plt.figure(figsize=(6, 4.5))
    plt.pie(stocks, labels=names, autopct="%1.1f%%", startangle=120)
    plt.title("Product Distribution by Stock")
    return _figure_to_base64()



def regression_chart(product_id: int, days_ahead: int, result: dict) -> str:
    """Generate a regression line chart for the given product prediction result."""
    x_train = result["x_train"]
    y_train = result["y_train"]
    x_future = result["x_future"]
    predicted = result["predicted_units"]

    plt.figure(figsize=(8, 4.5))
    plt.scatter(x_train, y_train, color="#2563eb", zorder=5, label="Actual Sales", s=60)

    if result["slope"] is not None and len(x_train) >= 2:
        x_range = np.linspace(min(x_train), x_future, 200)
        y_line = result["slope"] * x_range + result["intercept"]
        plt.plot(x_range, y_line, color="#7c3aed", linewidth=2, label="Regression Line")

    if x_future is not None and predicted is not None:
        plt.scatter(
            [x_future], [predicted],
            color="#ef4444", zorder=6, s=100,
            marker="*", label=f"Predicted (+{days_ahead}d): {predicted} units"
        )

    plt.title("Demand Prediction – Linear Regression")
    plt.xlabel("Day Index (days since first sale)")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.grid(alpha=0.2)
    return _figure_to_base64()


def dashboard_payload() -> dict:
    financials = profit_loss_analysis()
    line_chart = sales_line_chart()
    ml_predictions = predict_all_products(SALES_DATA, PRODUCTS, days_ahead=30)
    return {
        "total_products": len(PRODUCTS),
        "total_sales_qty": sum(int(item.get("qty", 0)) for item in SALES_DATA),
        "total_revenue": sum(float(item.get("total", 0.0)) for item in SALES_DATA),
        "fastest_product": PRODUCTS[0]["name"] if PRODUCTS else "N/A",
        "dead_stock": len([p for p in PRODUCTS if int(p.get("stock", 0)) == 0]),
        "ml_predictions": ml_predictions,
        "insights": [
            f"Stock Report generated for {len(PRODUCTS)} products",
            f"Current {financials['status']}: INR {abs(financials['profit']):.2f}",
        ],
        "chart_url": line_chart,
        "stock_status": stock_status_report(),
        "financials": financials,
        "stock_bar_chart": stock_bar_chart(),
        "sales_line_chart": line_chart,
        "stock_pie_chart": stock_pie_chart(),
    }
