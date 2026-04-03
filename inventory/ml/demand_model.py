from __future__ import annotations

from collections import defaultdict
from datetime import datetime

import numpy as np
from sklearn.linear_model import LinearRegression


def _build_time_series(sales_data: list[dict], product_id: int) -> tuple[list[int], list[int]]:
    """
    Aggregate sales quantities per calendar day for a given product.
    Returns (day_indices, quantities) where day_index=0 is the first sale day.
    """
    daily: dict[str, int] = defaultdict(int)
    for sale in sales_data:
        if int(sale.get("product_id", -1)) == product_id:
            ts = str(sale.get("timestamp", ""))
            day = ts.split(" ")[0] if ts else None
            if day:
                daily[day] += int(sale.get("qty", 0))

    if not daily:
        return [], []

    sorted_days = sorted(daily.keys())
    base = datetime.strptime(sorted_days[0], "%Y-%m-%d")
    day_indices = [(datetime.strptime(d, "%Y-%m-%d") - base).days for d in sorted_days]
    quantities = [daily[d] for d in sorted_days]
    return day_indices, quantities


def train_and_predict(
    sales_data: list[dict],
    product_id: int,
    days_ahead: int = 30,
) -> dict:
    """
    Train a Linear Regression model on past sales for a product and predict
    demand `days_ahead` days into the future from the last known sale date.

    Returns a dict with keys:
        predicted_units (int | None)
        r2_score        (float | None)
        data_points     (int)
        message         (str)
        x_train         (list[int])
        y_train         (list[int])
        x_future        (int)
        slope           (float | None)
        intercept       (float | None)
    """
    x_vals, y_vals = _build_time_series(sales_data, product_id)

    if len(x_vals) < 2:
        return {
            "predicted_units": None,
            "r2_score": None,
            "data_points": len(x_vals),
            "message": "Not enough data — need at least 2 sales records for this product.",
            "x_train": x_vals,
            "y_train": y_vals,
            "x_future": None,
            "slope": None,
            "intercept": None,
        }

    X = np.array(x_vals).reshape(-1, 1)
    y = np.array(y_vals)

    model = LinearRegression()
    model.fit(X, y)

    r2 = float(model.score(X, y))
    future_day = max(x_vals) + days_ahead
    predicted_raw = model.predict([[future_day]])[0]
    predicted_units = max(0, int(round(predicted_raw)))

    return {
        "predicted_units": predicted_units,
        "r2_score": round(r2, 4),
        "data_points": len(x_vals),
        "message": "Prediction successful.",
        "x_train": x_vals,
        "y_train": y_vals,
        "x_future": future_day,
        "slope": round(float(model.coef_[0]), 4),
        "intercept": round(float(model.intercept_), 4),
    }


def predict_all_products(sales_data: list[dict], products: list[dict], days_ahead: int = 30) -> list[dict]:
    """
    Run train_and_predict for every product and return a summary list.
    Each item: {product_id, product_name, predicted_units, r2_score, message}
    """
    results = []
    for p in products:
        pid = p["id"]
        result = train_and_predict(sales_data, pid, days_ahead)
        results.append(
            {
                "product_id": pid,
                "product_name": p["name"],
                "predicted_units": result["predicted_units"],
                "r2_score": result["r2_score"],
                "message": result["message"],
            }
        )
    return results


# Legacy compatibility – kept for any code that still calls predict_demand directly
def predict_demand(sales_data: list[dict]) -> int:
    total = sum(int(item.get("qty", 0)) for item in sales_data)
    return max(0, total)
