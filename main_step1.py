import torch
import torch.nn as nn
from data.generate_synthetic_data import generate_financial_graph_dataset
from engine.graph_builder import GraphDataPipeline
from engine.gnn_model import FinancialGraphSAGE

def run_step1_pipeline():
    print("⚡ [Step 1] Initializing Synthetic Financial Transaction Network...")
    nodes_df, tx_df = generate_financial_graph_dataset(num_nodes=500, num_legit_tx=2000)
    
    print("⚙️ [Step 1] Constructing Topological PyTorch Geometric Graph Object...")
    pipeline = GraphDataPipeline()
    graph_data = pipeline.build_pyg_graph(nodes_df, tx_df)
    
    print(f"   └── Graph Topology Built: {graph_data.num_nodes} Nodes | {graph_data.num_edges} Edges")
    
    print("🧠 [Step 1] Initializing FinancialGraphSAGE Neural Network Model...")
    model = FinancialGraphSAGE(in_channels=graph_data.num_node_features, hidden_channels=32)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    criterion = nn.BCELoss()

    # Train Model on Graph Topology
    model.train()
    print("🚀 [Step 1] Training Graph Neural Network on Structural Laundering Patterns...")
    for epoch in range(1, 101):
        optimizer.zero_grad()
        out = model(graph_data.x, graph_data.edge_index)
        loss = criterion(out, graph_data.y)
        loss.backward()
        optimizer.step()
        
        if epoch % 20 == 0:
            print(f"   └── Epoch {epoch:03d} | GNN Binary Cross-Entropy Loss: {loss.item():.4f}")

    # Evaluate Suspicious Nodes
    model.eval()
    with torch.no_grad():
        risk_scores = model(graph_data.x, graph_data.edge_index)
        
    print("\n🔍 [Step 1 Evaluation] Top 5 Highest Risk Accounts Flagged by GNN:")
    top_risk_indices = torch.argsort(risk_scores, descending=True)[:5]
    for idx in top_risk_indices:
        node_id = int(idx)
        score = float(risk_scores[node_id])
        actual_label = int(graph_data.y[node_id])
        print(f"   └── Node ID #{node_id:03d} | Anomaly Probability: {score:.4f} | Ground Truth Fraud: {actual_label}")

if __name__ == "__main__":
    run_step1_pipeline()