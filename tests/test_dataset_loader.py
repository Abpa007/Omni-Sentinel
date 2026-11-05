import pytest
from engine.dataset_loader import TransactionGraphDatasetLoader

def test_dataset_loader_initialization():
    loader = TransactionGraphDatasetLoader(num_nodes=200, num_features=10)
    data = loader.generate_synthetic_financial_network()
    
    assert data.num_nodes == 200
    assert data.x.size() == (200, 10)
    assert data.edge_index.size(0) == 2
    assert data.y.size(0) == 200
    
    summary = loader.get_summary(data)
    assert summary["num_nodes"] == 200
    assert summary["illicit_nodes_count"] > 0