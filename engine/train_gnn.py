import torch
import torch.nn.functional as F
from engine.dataset_loader import TransactionGraphDatasetLoader
from engine.gnn_model import OmniSentinelGNN

def train_and_evaluate_model(epochs: int = 50):
    print("🚀 Initializing Omni-Sentinel GNN Training Pipeline...")
    
    # 1. Load Dataset
    loader = TransactionGraphDatasetLoader(num_nodes=500, num_features=16)
    data = loader.generate_synthetic_financial_network()
    summary = loader.get_summary(data)
    print(f"📊 Graph Summary: {summary}")

    # 2. Initialize Model, Optimizer, and Loss Criterion
    model = OmniSentinelGNN(in_channels=16, hidden_channels=32, out_channels=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    criterion = torch.nn.CrossEntropyLoss()

    # 3. Training Loop
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}] | Loss: {loss.item():.4f}")

    # 4. Evaluation Loop
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        pred = out.argmax(dim=1)
        correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
        acc = int(correct) / int(data.test_mask.sum())
        print(f"✅ Training Complete! Test Accuracy: {acc * 100:.2f}%")

    return model, acc

if __name__ == "__main__":
    train_and_evaluate_model()