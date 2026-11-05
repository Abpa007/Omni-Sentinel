import os
from neo4j import GraphDatabase

class OmniNeo4jStore:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        """
        Initializes connection to the Neo4j graph database instance.
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        except Exception as e:
            print(f"⚠️ [Neo4j Warning] Could not connect to Neo4j instance: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def sync_networkx_to_neo4j(self, G):
        """
        Syncs NetworkX graph nodes and transaction edges into Neo4j graph storage.
        """
        if not self.driver:
            print("❌ Neo4j driver not initialized.")
            return

        with self.driver.session() as session:
            # Create/Merge Accounts (Nodes)
            for node, data in G.nodes(data=True):
                session.run(
                    """
                    MERGE (a:Account {id: $node_id})
                    SET a.is_fraud = $is_fraud, a.risk_score = $risk_score
                    """,
                    node_id=int(node),
                    is_fraud=bool(data.get("is_fraud", False)),
                    risk_score=float(data.get("risk_score", 0.0))
                )

            # Create/Merge Transactions (Edges)
            for u, v, data in G.edges(data=True):
                session.run(
                    """
                    MATCH (a:Account {id: $u})
                    MATCH (b:Account {id: $v})
                    MERGE (a)-[r:TRANSACTION {tx_id: $tx_id}]->(b)
                    SET r.amount = $amount, r.timestamp = $timestamp
                    """,
                    u=int(u),
                    v=int(v),
                    tx_id=int(data.get("tx_id", 0)),
                    amount=float(data.get("amount", 0.0)),
                    timestamp=int(data.get("timestamp", 0))
                )
        print("✅ Successfully synced network topology to Neo4j graph store!")

    def save_forensic_dossier(self, node_id: int, dossier: dict):
        """
        Persists an automated LangGraph forensic audit dossier directly to the target node in Neo4j.
        """
        if not self.driver:
            return

        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Account {id: $node_id})
                SET a.audit_verdict = $verdict,
                    a.audit_action = $action,
                    a.compliance_flags = $flags,
                    a.last_audited = timestamp()
                """,
                node_id=int(node_id),
                verdict=dossier.get("verdict", ""),
                action=dossier.get("action", ""),
                flags=dossier.get("compliance_flags", [])
            )
        print(f"✅ Persistent forensic dossier saved to Neo4j for Account #{node_id}")