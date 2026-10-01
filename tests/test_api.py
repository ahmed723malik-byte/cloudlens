"""Tests for CloudLens API endpoints."""

import pytest
from app import create_app
from app.config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as c:
        yield c


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_resources_returns_list(client):
    res = client.get("/api/resources")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_resource_schema(client):
    data = client.get("/api/resources").get_json()
    required = {"id", "name", "provider", "resource_type", "region",
                "monthly_cost", "utilisation_pct", "cost_efficiency_score"}
    for resource in data:
        assert required.issubset(resource.keys()), f"Missing keys in {resource}"


def test_costs_summary(client):
    res = client.get("/api/costs")
    assert res.status_code == 200
    data = res.get_json()
    assert "total_monthly" in data
    assert "by_provider" in data
    assert data["total_monthly"] > 0
    for provider in ("AWS", "GCP", "Azure"):
        assert provider in data["by_provider"]


def test_optimisations(client):
    res = client.get("/api/optimisations")
    assert res.status_code == 200
    data = res.get_json()
    assert "recommendations" in data
    assert "total_potential_saving" in data
    assert data["total_potential_saving"] >= 0


def test_optimisation_schema(client):
    recs = client.get("/api/optimisations").get_json()["recommendations"]
    required = {"resource_id", "resource_name", "severity", "title",
                "description", "estimated_monthly_saving", "action"}
    for rec in recs:
        assert required.issubset(rec.keys())
        assert rec["severity"] in ("high", "medium", "low")


def test_patterns(client):
    res = client.get("/api/patterns")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 3
    for p in data:
        assert "name" in p
        assert "components" in p
        assert len(p["components"]) > 0


def test_index_renders(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"CloudLens" in res.data
