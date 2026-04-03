from __future__ import annotations


def predict_demand(sales_data: list[dict]) -> int:
    """Return a simple placeholder demand prediction from current sales quantity."""
    recent_qty = sum(int(item.get("qty", 0)) for item in sales_data)
    return max(100, recent_qty)
