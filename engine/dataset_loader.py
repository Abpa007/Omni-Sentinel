import torch
import numpy as np
from torch_geometric.data import Data
from typing import Tuple, Dict, Any

class TransactionGraphDatasetLoader:
    def __init__(self, num_nodes: int = 500, num_features: int = 16):
        """
        Initializes the synthetic/real-world hybrid transaction graph loader 
        compatible with PyTorch Geometric (PyG) standards.
        """
        self.num_nodes = num_nodes
        self.num_features = num_features

    def generate_synthetic_financial_network(self) -> Data:
        """
        Generates a robust transaction graph simulating accounts (nodes) and 
        money transfers (edges), pre-configured with anomaly labels for GNN training.
        """
        torch.manual_seed(42)
        np.random.seed(42)

        # 1. Node Feature Matrix X [num_nodes, num_features]
        x = torch.randn(self.num_nodes, self.num_features, dtype=torch.float)

        # Inject specific patterns for known laundering clusters / shell rings (e.g., node 45, 88, 422)
        high_risk_nodes = [45, 88, 422, 12, 150]
        for node in high_risk_nodes:
            if node < self.num_nodes:
                x[node] += torch.randn(self.num_features) * 3.0  # Anomaly signature shift

        # 2. Edge Index [2, num_edges] (Directed transaction flows)
        sources, targets = [], []
        # Normal sequential/random transactions
        for i in range(self.num_nodes):
            # Connect to 3-5 random neighboring accounts
            num_neighbors = np.random.randint(2, 6)
            neighbors = np.random.choice(self.num_nodes, num_neighbors, replace=False)
            for n in neighbors:
                if n != i:
                    sources.append(i)
                    targets.append(n)

        # Inject dense loops/syndicates for high-risk nodes
        syndicate_core = [45, 88, 422]
        for s in syndicate_core:
            for t in syndicate_core:
                if s != t:
                    sources.append(s)
                    targets.append(t)

        edge_index = torch.tensor([sources, targets], dtype=torch.long)

        # 3. Target Labels Y (0: Licit, 1: Illicit / AML Risk)
        y = torch.zeros(self.num_nodes, dtype=torch.long)
        for node in high_risk_nodes:
            if node < self.num_nodes:
                y[node] = 1

        # 4. Train / Test Masks
        train_mask = torch.zeros(self.num_nodes, dtype=torch.bool)
        test_mask = torch.zeros(self.num_nodes, dtype=torch.bool)
        
        # 80% train, 20% test split
        split_idx = int(0.8 * self.num_nodes)
        train_mask[:split_idx] = True
        test_mask[split_idx:] = True

        data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, test_mask=test_mask)
        return data

    def get_summary(self, data: Data) -> Dict[str, Any]:
        return {
            "num_nodes": data.num_nodes,
            "num_edges": data.edge_index.size(1),
            "num_features": data.num_node_features,
            "illicit_nodes_count": int(data.y.sum().item()),
            "fraud_rate_pct": float((data.y.sum().item() / data.num_nodes) * 100)
        }