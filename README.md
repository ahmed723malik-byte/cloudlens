# CloudLens 🔭

> Multi-cloud infrastructure visualiser and cost optimisation dashboard

[![CI](https://github.com/ahmed723malik-byte/cloudlens/actions/workflows/ci.yml/badge.svg)](https://github.com/ahmed723malik-byte/cloudlens/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.1-green)](https://flask.palletsprojects.com)

CloudLens provides unified visibility across AWS, GCP, and Azure — surfacing cost breakdowns, underutilised resources, and reference architecture patterns in a single dashboard.

---

## Features

- **Multi-cloud overview** — spend by provider, resource type, and environment  
- **Resource inventory** — filterable table with utilisation and efficiency scoring  
- **Cost forecasting** — 12-month projection per cloud provider  
- **Optimisation engine** — flags underutilised resources with estimated savings  
- **Architecture patterns** — reference designs for serverless, containers, data pipelines, and HA multi-region setups  

## Architecture

```
cloudlens/
├── app/
│   ├── __init__.py       # Application factory
│   ├── config.py         # Environment configs
│   ├── models.py         # Resource & recommendation dataclasses
│   ├── services.py       # Cloud data layer (swap for real SDK calls)
│   ├── routes.py         # Flask blueprints
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       └── index.html
├── tests/
│   └── test_api.py
├── .github/workflows/ci.yml
├── requirements.txt
├── Procfile
└── run.py
```

## Quick Start

```bash
git clone https://github.com/ahmed723malik-byte/cloudlens.git
cd cloudlens
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open [http://localhost:5000](http://localhost:5000)

## Running Tests

```bash
pytest tests/ -v
```

## Connecting Real Cloud Providers

The `CloudService` in `app/services.py` uses mock data by default. To connect live accounts:

**AWS** — replace `MOCK_RESOURCES` with calls to `boto3`:
```python
import boto3
ce = boto3.client('ce', region_name='eu-west-1')
# Cost Explorer: get_cost_and_usage(...)
# EC2: describe_instances(...)
```

**GCP** — use `google-cloud-billing` and `google-cloud-asset`:
```python
from google.cloud import billing_v1
client = billing_v1.CloudBillingClient()
```

**Azure** — use `azure-mgmt-costmanagement`:
```python
from azure.mgmt.costmanagement import CostManagementClient
```

## Deployment

Deploy to Render, Railway, or Heroku with a single command — the `Procfile` runs `gunicorn` automatically.

```bash
# Set production env
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask 3.1 |
| Frontend | Vanilla JS, Chart.js 4 |
| Testing | pytest, pytest-flask |
| CI/CD | GitHub Actions |
| Deploy | Gunicorn + Render/Heroku |

---

Built to demonstrate cloud architecture patterns, cost management thinking, and Python application structure.
