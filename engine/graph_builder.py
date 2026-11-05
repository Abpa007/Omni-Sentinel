import torch
import pandas as pd
import numpy as np
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler

class GraphDataPipeline:
    def __init__(self):
        self.scaler = StandardScaler()

    def build_pyg_graph(self, nodes_df: pd.DataFrame, tx_df: pd.DataFrame) -> Data:
        # Encode Node Features
        node_type_map = {"INDIVIDUAL": 0, "SHELL_CORP": 1, "EXCHANGE": 2, "MERCHANT": 3}
        nodes_df["type_code"] = nodes_df["account_type"].map(node_type_map)
        
        raw_features = nodes_df[["type_code", "account_age_days", "kyc_verified", "avg_daily_volume"]].values
        scaled_features = self.scaler.fit_transform(raw_features)
        
        x = torch.tensor(scaled_features, dtype=torch.float)
        
        # Build Edge Index (Source -> Target)
        edge_src = torch.tensor(tx_df["source"].values, dtype=torch.long)
        edge_dst = torch.tensor(tx_df["target"].values, dtype=torch.long)
        edge_index = torch.stack([edge_src, edge_dst], dim=0)
        
        # Build Edge Attributes (Amount, timestamp)
        edge_attr = torch.tensor(
            np.column_stack([tx_df["amount"].values, tx_df["timestamp"].values]), 
            dtype=torch.float
        )
        
        # Node Labels (Node is marked fraudulent if involved in any fraud transaction)
        fraud_nodes = set(tx_df[tx_df["is_fraud"] == 1]["source"].tolist() + tx_df[tx_df["is_fraud"] == 1]["target"].tolist())
        y = torch.tensor([1 if n in fraud_nodes else 0 for n in nodes_df["node_id"].values], dtype=torch.float)

        graph_data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)
        return graph_data