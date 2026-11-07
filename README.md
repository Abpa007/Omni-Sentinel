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
