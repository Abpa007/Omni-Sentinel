import numpy as np
import pandas as pd
import json

def generate_financial_graph_dataset(num_nodes=500, num_legit_tx=2000, seed=42):
    np.random.seed(seed)
    nodes = []
    
    # 1. Generate Nodes (Accounts/Wallets)
    for i in range(num_nodes):
        nodes.append({
            "node_id": i,
            "account_type": np.random.choice(["INDIVIDUAL", "SHELL_CORP", "EXCHANGE", "MERCHANT"]),
            "account_age_days": int(np.random.randint(1, 3650)),
            "kyc_verified": int(np.random.choice([0, 1], p=[0.2, 0.8])),
            "avg_daily_volume": float(np.random.exponential(scale=1000.0))
        })
    
    transactions = []
    tx_id = 0
    
    # 2. Generate Normal Transactions
    for _ in range(num_legit_tx):
        src = np.random.randint(0, num_nodes)
        dst = np.random.randint(0, num_nodes)
        if src != dst:
            transactions.append({
                "tx_id": tx_id,
                "source": src,
                "target": dst,
                "amount": round(float(np.random.exponential(scale=500.0) + 10), 2),
                "timestamp": int(np.random.randint(1600000000, 1700000000)),
                "is_fraud": 0
            })
            tx_id += 1
            
    # 3. Inject Fraud Pattern A: Circular Money Ring (Node A -> B -> C -> A)
    ring_nodes = [45, 112, 203, 399]
    ring_amount = 49500.0
    for i in range(len(ring_nodes)):
        src = ring_nodes[i]
        dst = ring_nodes[(i + 1) % len(ring_nodes)]
        transactions.append({
            "tx_id": tx_id,
            "source": src,
            "target": dst,
            "amount": ring_amount,
            "timestamp": 1690000000 + i * 300,
            "is_fraud": 1
        })
        tx_id += 1

    # 4. Inject Fraud Pattern B: Smurfing / Fan-Out (One source splitting funds to many)
    mule_master = 88
    mules = [12, 19, 77, 140, 290, 310]
    for m in mules:
        transactions.append({
            "tx_id": tx_id,
            "source": mule_master,
            "target": m,
            "amount": 9800.0,
            "timestamp": 1695000000,
            "is_fraud": 1
        })
        tx_id += 1

    df_nodes = pd.DataFrame(nodes)
    df_tx = pd.DataFrame(transactions)
    
    return df_nodes, df_tx

if __name__ == "__main__":
    nodes_df, tx_df = generate_financial_graph_dataset()
    nodes_df.to_csv("nodes.csv", index=False)
    tx_df.to_csv("transactions.csv", index=False)
    print(f"Generated {len(nodes_df)} nodes and {len(tx_df)} transactions (including injected fraud rings).")