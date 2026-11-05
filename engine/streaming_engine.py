import asyncio
import json
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from engine.agent_swarm import OmniSentinelSwarm

app = FastAPI(title="Omni-Sentinel Financial Forensics Gateway", version="1.0.0")

# Initialize Agent Swarm
swarm = OmniSentinelSwarm()

# WebSocket Connection Manager for Live Telemetry
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                pass

manager = ConnectionManager()

class TransactionPayload(BaseModel):
    tx_id: int
    source_node: int
    target_node: int
    amount: float
    timestamp: int

@app.get("/")
def health_check():
    return {"status": "online", "system": "Omni-Sentinel Real-Time Financial Forensics Mesh"}

@app.post("/api/v1/ingest")
async def ingest_transaction(tx: TransactionPayload):
    """
    Ingests a live transaction, calculates risk via GNN heuristics, 
    and dispatches the LangGraph agent swarm if high-risk.
    """
    # Simulate GNN real-time scoring based on transaction characteristics
    # (In production, this feeds into our trained GraphSAGE model tensors)
    simulated_risk_score = 0.92 if tx.amount > 40000 or tx.source_node in [45, 88] else 0.15
    
    alert_triggered = simulated_risk_score > 0.8
    dossier = None

    if alert_triggered:
        # Automatically trigger the LangGraph multi-agent forensic investigation swarm
        agent_result = swarm.run_investigation(node_id=tx.source_node, risk_score=simulated_risk_score)
        dossier = {
            "target_node": agent_result["node_id"],
            "risk_score": agent_result["risk_score"],
            "compliance_flags": agent_result["compliance_flags"],
            "verdict": agent_result["final_verdict"],
            "action": agent_result["action_recommended"],
            "logs": agent_result["investigation_logs"]
        }
        
        # Broadcast live alert to all connected dashboard clients via WebSocket
        await manager.broadcast({
            "event": "CRITICAL_THREAT_DETECTED",
            "tx_id": tx.tx_id,
            "dossier": dossier
        })

    return {
        "status": "processed",
        "tx_id": tx.tx_id,
        "risk_score": simulated_risk_score,
        "threat_detected": alert_triggered,
        "forensic_dossier": dossier
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client heartbeats/messages
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({"received": data, "status": "connected"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)