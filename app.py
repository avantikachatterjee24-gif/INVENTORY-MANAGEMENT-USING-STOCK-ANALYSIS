from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

products = [
    {"id": 1, "name": "Product A", "stock": 50, "price": 29.99, "expiry_date": "2026-03-30"},
    {"id": 2, "name": "Product B", "stock": 30, "price": 19.99, "expiry_date": "2026-03-25"},
]

sales_data = [
    {"id": 1, "product_id": 1, "product_name": "Product A", "qty": 5, "total": 149.95, "timestamp": "2024-10-15 10:30"},
    {"id": 2, "product_id": 2, "product_name": "Product B", "qty": 3, "total": 59.97, "timestamp": "2024-10-16 14:20"},
]

@app.route('/')
def home():
    stats = {
        "total_sales": sum(int(s.get('qty', 0)) for s in sales_data),
        "total_revenue": sum(float(s.get('total', 0.0)) for s in sales_data)
    }
    return render_template('index.html', stats=stats)

@app.route('/dashboard')
def dashboard():
    analytics = {
        "total_products": len(products),
        "total_sales_qty": sum(int(s.get('qty', 0)) for s in sales_data),
        "total_revenue": sum(float(s.get('total', 0.0)) for s in sales_data),
        "fastest_product": "Product A",
        "dead_stock": 0,
        "ml_predicted_demand": 100,
        "insights": ["System running smoothly"],
        "ml_comparison": [{"day": "Day 1", "actual": 5, "predicted": 6}],
        "chart_url": ""
    }
    alerts = [{"type": "success", "message": "All good"}]
    return render_template('dashboard.html', analytics=analytics, alerts=alerts)

@app.route('/products')
def products():
    days_left = {}
    for product in products:
        expiry = datetime.strptime(product["expiry_date"], "%Y-%m-%d")
        today = datetime.now()
        diff = (expiry - today).days
        days_left[product["id"]] = diff
    return render_template('products.html', products=products, days_left=days_left)

@app.route('/sales', methods=['GET', 'POST'])
def sales_route():
    global sales_data
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        qty = int(request.form['qty'])
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            total = qty * product['price']
            new_sale = {
                "id": len(sales_data) + 1,
                "product_id": product_id,
                "product_name": product['name'],
                "qty": qty,
                "total": round(total, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            sales_data.append(new_sale)
        return redirect(url_for('sales_route'))
    stats = {
        "total_sales": sum(int(s.get('qty', 0)) for s in sales_data),
        "total_revenue": sum(float(s.get('total', 0.0)) for s in sales_data)
    }
    return render_template('sales.html', products=products, sales_list=sales_data, stats=stats)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name', '')
    stock = int(request.form.get('stock', 0))
    price = float(request.form.get('price', 0.0))
    new_id = len(products) + 1
    products.append({"id": new_id, "name": name, "stock": stock, "price": price, "expiry_date": "2026-12-31"})
    return redirect(url_for('products'))

@app.route('/update_product', methods=['POST'])
def update_product():
    pid = int(request.form.get('id', 0))
    for p in products:
        if p['id'] == pid:
            p['name'] = request.form.get('name', p['name'])
            p['stock'] = int(request.form.get('stock', p['stock']))
            p['price'] = float(request.form.get('price', p['price']))
            break
    return redirect(url_for('products'))

@app.route('/delete_product/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    global products
    products[:] = [p for p in products if p['id'] != pid]  # In-place to avoid global reassign
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
