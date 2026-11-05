import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class FinancialGraphSAGE(nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int = 1):
        super(FinancialGraphSAGE, self).__init__()
        # Layer 1: Aggregate 1st-degree neighbors
        self.conv1 = SAGEConv(in_channels, hidden_channels, aggr="mean")
        # Layer 2: Aggregate 2nd-degree neighbors (detects multi-hop circular loops)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels, aggr="max")
        
        self.fc = nn.Linear(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        # First Graph Convolution Step
        h = self.conv1(x, edge_index)
        h = F.relu(h)
        h = F.dropout(h, p=0.2, training=self.training)
        
        # Second Graph Convolution Step
        h = self.conv2(h, edge_index)
        h = F.relu(h)
        
        # Final Risk Score (Sigmoid for probability 0.0 -> 1.0)
        out = self.fc(h)
        return torch.sigmoid(out).squeeze(-1)