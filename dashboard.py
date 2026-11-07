import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Omni-Sentinel | Financial Forensics Mesh",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Enterprise Light Theme CSS for Crystal-Clear Visibility
st.markdown("""
<style>
    /* Main App Background - Clean Light Slate */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    /* Header Container styling */
    .sentinel-header {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        padding: 28px 32px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        margin-bottom: 24px;
    }
    .sentinel-title {
        font-size: 30px;
        font-weight: 800;
        color: #1e40af;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .sentinel-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Metric Cards Styling */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .metric-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        font-weight: 700;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 8px;
    }
    .metric-badge-green {
        font-size: 12px;
        color: #16a34a;
        font-weight: 700;
        margin-top: 6px;
    }
    .metric-badge-red {
        font-size: 12px;
        color: #dc2626;
        font-weight: 700;
        margin-top: 6px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        color: #334155;
        font-weight: 700;
        padding: 10px 20px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background: #2563eb !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="sentinel-header">
    <div class="sentinel-title">🛡️ OMNI-SENTINEL FORENSICS MESH</div>
    <div class="sentinel-subtitle">Enterprise Graph Intelligence & Real-Time Threat Detection Swarm</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Console
with st.sidebar:
    st.markdown("### 🎛️ Swarm Command Console")
    scan_mode = st.selectbox("Detection Engine", ["Real-time GNN Swarm", "Historical Batch Analysis", "Topology Deep Scan"])
    sensitivity = st.slider("Anomaly Sensitivity Threshold", 0.0, 1.0, 0.75)
    auto_persist = st.toggle("Neo4j Persistence Layer", value=True)
    
    st.divider()
    st.markdown("### 🟢 System Telemetry")
    st.markdown("• **Neo4j DB:** `Connected`\n• **GNN Engine:** `Active (PyTorch)`\n• **Swarm Latency:** `4.2ms`")

# Top KPI Metric Cards Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Total Transactions</div>
        <div class="metric-val">1,248,920</div>
        <div class="metric-badge-green">↑ 12.4% vs previous 24h</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Flagged Anomalies</div>
        <div class="metric-val">142</div>
        <div class="metric-badge-red">⚠️ 18 High-Confidence Threats</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">High Risk Exposure</div>
        <div class="metric-val">$482,150</div>
        <div class="metric-badge-red">Requires Immediate Audit</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Inference Throughput</div>
        <div class="metric-val">4.2 ms</div>
        <div class="metric-badge-green">⚡ Real-time Stream Active</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 Live Forensics Stream", "🌐 Graph Subgraph Topology", "🤖 Autonomous Swarm Logs"])

with tab1:
    st.subheader("Live High-Risk Transaction Feed")
    
    df = pd.DataFrame({
        "Tx ID": [101, 102, 103, 104, 105],
        "Source Account": ["Acc_1001", "Acc_4509", "Acc_8821", "Acc_1102", "Acc_9904"],
        "Target Account": ["Acc_2002", "Acc_7731", "Acc_3310", "Acc_6641", "Acc_5582"],
        "Amount ($)": [1500.50, 48200.00, 120.00, 95400.00, 310.00],
        "GNN Risk Score": [0.85, 0.94, 0.12, 0.98, 0.05],
        "Verdict": ["Flagged", "Escalated", "Passed", "Blocked", "Passed"]
    })
    
    st.dataframe(df, width="stretch", hide_index=True)

with tab2:
    st.subheader("Neo4j Graph Relationship Cluster")
    st.info("Visualizing interconnected account clusters tied to flagged transaction nodes in `bolt://localhost:7687`.")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Risk Velocity', 'Degree Centrality', 'Amount Variance'])
    st.line_chart(chart_data, width="stretch")

with tab3:
    st.subheader("Swarm Agent Activity Log")
    st.code("""
[08:14:02] [INFO] Agent-1 (Ingestion): Polling live transaction stream batch...
[08:14:02] [INFO] Agent-2 (GNN Core): Executing GraphSAGE message passing across 1,420 nodes...
[08:14:03] [WARN] Agent-2 (GNN Core): Structural anomaly detected on Tx #104 (Risk Score: 0.98).
[08:14:03] [INFO] Agent-3 (Persistence): Writing cypher transaction node to Neo4j database...
[08:14:03] [SUCCESS] Agent-3 (Persistence): Successfully logged relationship: (Acc_1102)-[:TRANSFER]->(Acc_6641).
    """, language="bash")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    