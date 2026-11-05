import pytest
from fastapi.testclient import TestClient
from engine.streaming_engine import app, gnn_model

client = TestClient(app)

def test_system_startup_and_gnn():
    """Verifies that the FastAPI application starts up and loads the GNN model."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["gnn_active"] is True

def test_high_risk_transaction_pipeline():
    """Verifies end-to-end ingestion, GNN scoring, agent swarm, and persistence triggers."""
    payload = {
        "tx_id": 9001,
        "source_node": 45,  # High risk syndicate node
        "target_node": 112,
        "amount": 75000.0,
        "timestamp": 1690000000
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "processed"
    assert data["threat_detected"] is True
    assert data["risk_score"] > 0.8
    assert data["forensic_dossier"] is not None
    assert data["forensic_dossier"]["target_node"] == 45
    assert len(data["forensic_dossier"]["compliance_flags"]) > 0