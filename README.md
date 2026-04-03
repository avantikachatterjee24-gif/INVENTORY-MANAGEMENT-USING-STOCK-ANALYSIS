# EDI Inventory System

This project is now organized into a modular Flask structure.

## Folder Structure

```
.
|-- app.py
|-- requirements.txt
|-- inventory/
|   |-- __init__.py
|   |-- routes.py
|   |-- data/
|   |   |-- __init__.py
|   |   `-- store.py
|   |-- services/
|   |   |-- __init__.py
|   |   `-- analytics.py
|   |-- database/
|   |   |-- __init__.py
|   |   |-- db.py
|   |   `-- schema.sql
|   |-- ml/
|   |   |-- __init__.py
|   |   `-- demand_model.py
|   |-- templates/
|   |   |-- base.html
|   |   |-- index.html
|   |   |-- dashboard.html
|   |   |-- products.html
|   |   |-- sales.html
|   |   `-- macros.html
|   `-- static/
|       `-- style.css
|-- TODO.md
```

## Routes

- `/` -> Landing page
- `/dashboard` -> Analytics dashboard
- `/products` -> Product inventory management
- `/sales` -> Sales tracking and recording
- `/generate_dummy_data` -> Placeholder endpoint for dashboard action

## Layers

- `inventory/routes.py`: HTTP routes and request/response handling
- `inventory/data/store.py`: In-memory inventory and sales storage
- `inventory/services/analytics.py`: Business calculations for stats and dashboard payload
- `inventory/ml/demand_model.py`: ML placeholder logic for demand prediction
- `inventory/database/`: Database connection and schema placeholders for migration to persistent storage

## Run

```bash
python3 app.py
```

Open http://127.0.0.1:5050.

Note: On macOS, port 5000 may be occupied by AirPlay Receiver. This project uses port 5050 by default. You can override it with the `PORT` environment variable.
