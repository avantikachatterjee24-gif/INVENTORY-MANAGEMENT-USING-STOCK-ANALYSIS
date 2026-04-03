from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for

from inventory.data.store import (
    PRODUCTS,
    SALES_DATA,
    add_product,
    append_sale,
    delete_product,
    update_product,
)
from inventory.ml.demand_model import train_and_predict
from inventory.services.analytics import dashboard_payload, product_days_left, regression_chart, sales_stats

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html", stats=sales_stats())


@main_bp.route("/dashboard")
def dashboard():
    alerts = [{"type": "success", "message": "All good"}]
    return render_template("dashboard.html", analytics=dashboard_payload(), alerts=alerts)


@main_bp.route("/products")
def products_page():
    return render_template("products.html", products=PRODUCTS, days_left=product_days_left())


@main_bp.route("/sales", methods=["GET", "POST"])
def sales_route():
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        qty = int(request.form["qty"])
        product = next((item for item in PRODUCTS if item["id"] == product_id), None)
        if product and qty > 0 and int(product.get("stock", 0)) >= qty:
            append_sale(product_id, product["name"], qty, float(product["price"]))
            product["stock"] = int(product.get("stock", 0)) - qty
        return redirect(url_for("main.sales_route"))

    return render_template(
        "sales.html",
        products=PRODUCTS,
        sales_list=SALES_DATA,
        stats=sales_stats(),
    )


@main_bp.route("/add_product", methods=["POST"])
def add_product_route():
    name = request.form.get("name", "").strip()
    stock = int(request.form.get("stock", 0))
    price = float(request.form.get("price", 0.0))
    cost_price = float(request.form.get("cost_price", round(price * 0.6, 2)))
    if name:
        add_product(name=name, stock=stock, price=price, cost_price=cost_price)
    return redirect(url_for("main.products_page"))


@main_bp.route("/update_product", methods=["POST"])
def update_product_route():
    pid = int(request.form.get("id", 0))
    name = request.form.get("name", "").strip()
    stock = int(request.form.get("stock", 0))
    price = float(request.form.get("price", 0.0))
    cost_price = float(request.form.get("cost_price", round(price * 0.6, 2)))
    if name:
        update_product(pid=pid, name=name, stock=stock, price=price, cost_price=cost_price)
    return redirect(url_for("main.products_page"))


@main_bp.route("/delete_product/<int:pid>", methods=["DELETE"])
def delete_product_route(pid: int):
    delete_product(pid)
    return "", 204


@main_bp.route("/generate_dummy_data")
def generate_dummy_data():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/predict", methods=["GET", "POST"])
def predict_route():
    result = None
    chart_b64 = None
    selected_product_id = None
    days_ahead = 30

    if request.method == "POST":
        selected_product_id = int(request.form.get("product_id", 0))
        days_ahead = max(1, min(365, int(request.form.get("days_ahead", 30))))
        result = train_and_predict(SALES_DATA, selected_product_id, days_ahead)
        if result["predicted_units"] is not None:
            chart_b64 = regression_chart(selected_product_id, days_ahead, result)

    return render_template(
        "predict.html",
        products=PRODUCTS,
        result=result,
        chart_b64=chart_b64,
        selected_product_id=selected_product_id,
        days_ahead=days_ahead,
    )
