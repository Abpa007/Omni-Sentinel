import pytest
from fastapi.testclient import TestClient
from engine.streaming_engine import app
from engine.agent_swarm import OmniSentinelSwarm

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_agent_swarm_execution():
    swarm = OmniSentinelSwarm()
    result = swarm.run_investigation(node_id=45, risk_score=0.92)
    assert result["node_id"] == 45
    assert "CRITICAL THREAT" in result["final_verdict"]
    assert len(result["compliance_flags"]) > 0

def test_transaction_ingest_high_risk():
    payload = {
        "tx_id": 1001,
        "source_node": 45,
        "target_node": 112,
        "amount": 50000.0,
        "timestamp": 1690000000
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert data["threat_detected"] is True
    assert data["risk_score"] > 0.8
    assert "forensic_dossier" in data

def test_transaction_ingest_low_risk():
    payload = {
        "tx_id": 1002,
        "source_node": 10,
        "target_node": 15,
        "amount": 250.0,
        "timestamp": 1690000000
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert data["threat_detected"] is False
    assert data["forensic_dossier"] is None