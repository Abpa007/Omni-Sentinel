import os
from dotenv import load_dotenv
from neo4j import GraphDatabase, exceptions

# Load environment variables from .env file
load_dotenv()

class Neo4jConnector:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize Neo4j driver: {e}")

    def verify_connectivity(self):
        """Verifies connection to the Neo4j database instance."""
        if not self.driver:
            return False
        try:
            self.driver.verify_connectivity()
            return True
        except exceptions.ServiceUnavailable:
            return False
        except Exception as e:
            print(f"Neo4j connectivity error: {e}")
            return False

    def log_transaction(self, tx_id: int, source_node: int, target_node: int, amount: float, risk_score: float):
        """Logs a financial transaction and links accounts in the Neo4j graph."""
        if not self.driver:
            return False
        
        query = """
        MERGE (s:Account {id: $source_node})
        MERGE (t:Account {id: $target_node})
        CREATE (s)-[:TRANSACTION {
            tx_id: $tx_id,
            amount: $amount,
            risk_score: $risk_score,
            timestamp: datetime()
        }]->(t)
        """
        try:
            with self.driver.session() as session:
                session.run(query, source_node=source_node, target_node=target_node, tx_id=tx_id, amount=amount, risk_score=risk_score)
            return True
        except Exception as e:
            print(f"Failed to log transaction to Neo4j: {e}")
            return False

    def close(self):
        if self.driver:
            self.driver.close()