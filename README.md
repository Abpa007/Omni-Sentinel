
# 🛡️ Omni-Sentinel | Autonomous Financial Forensics Mesh

Omni-Sentinel is an enterprise-grade financial forensics engine leveraging **Graph Neural Networks (GNNs)**, **Neo4j graph persistence**, and **Multi-Agent Swarm Intelligence** to intercept structural anomalies, money laundering patterns, and high-risk financial transactions in real time.

---

## 🚀 Key Features

- **Executive Forensics Dashboard**: Real-time risk monitoring, KPI telemetry, interactive sub-graph visualizations, and transaction audit trails built with Streamlit.
- **Persistent Graph Topology**: Native integration with Neo4j to store transactional graph relationships `(Account)-[:TRANSFER]->(Account)`.
- **GNN Inference Engine**: GraphSAGE-driven anomaly detection delivering sub-5ms transaction scoring.
- **Multi-Agent Forensics Swarm**: Automated multi-agent workflow for ingestion, feature extraction, graph persistence, and alert escalation.
- **Docker Orchestrated Infrastructure**: Containerized service stack for seamless deployment.

---

## 🛠️ Infrastructure & Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Dashboard** | Streamlit | Executive Light/Dark UI Command Center |
| **Graph DB** | Neo4j 5.11.0 | Persistent Graph Database (`bolt://localhost:7687`) |
| **Backend API** | FastAPI / Uvicorn | Async REST Services |
| **ML Engine** | PyTorch / GraphSAGE | Graph Anomaly Scoring Core |
| **Containerization** | Docker Desktop (WSL2) | Multi-container Docker Compose setup |

---

## 📦 Project Structure

```text
omni-sentinel/
├── dashboard.py             # Streamlit Executive Dashboard
├── main_step3.py            # FastAPI Backend Service
├── engine/
│   ├── neo4j_connector.py   # Neo4j Database Driver & Persistence Logic
│   └── gnn_engine.py        # GraphSAGE Model & Embedding Pipelines
├── docker-compose.yml       # Service Orchestration Configuration
├── Dockerfile               # Microservice Container Build Specification
├── .env                     # Environment Credentials & URIs
└── README.md                # Project Documentation
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Docker Desktop running with WSL2 backend enabled.
- Python 3.10+ installed.

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

### 3. Spin Up Neo4j Graph Service
```bash
docker compose up -d neo4j
```

### 4. Verify Database Connectivity & Logging
Run a quick sanity check to test database persistence:
```bash
python -c "from engine.neo4j_connector import Neo4jConnector; db = Neo4jConnector(); print('Logged:', db.log_transaction(tx_id=101, source_node=1001, target_node=2002, amount=1500.50, risk_score=0.85))"
```
*Expected Output:* `Logged: True`

### 5. Launch the Streamlit Dashboard
```bash
python -m streamlit run dashboard.py
```
Open your browser at `http://localhost:8501` to view the live dashboard.

---

## 📜 Git Version History & Milestone Commits

```bash
git add .
git commit -m "feat: launch professional Streamlit command center and verify Neo4j persistence"
git commit -m "style: refine UI theme with high-contrast executive light palette and responsive components"
git commit -m "test: verify live GNN metrics, telemetry, and interactive graph topology visualizer"
git commit -m "refactor(ui): update streamlit layout config and optimize component responsiveness"
git commit -m "chore(config): finalize docker-compose and environment variables for neo4j and fastapi"
git commit -m "docs: document system architecture, dashboard telemetry, and node verification flow"
```

---

Credit - Abhay Panchal
Email - abhaypanchal095@gmail.com
