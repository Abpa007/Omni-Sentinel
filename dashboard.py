import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title="Omni-Sentinel | Financial Forensics Command Center",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Omni-Sentinel: Autonomous Financial Forensics & Threat Intelligence Mesh")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("🕹️ Simulation & Control Center")
target_node = st.sidebar.number_input("Target Account / Node ID", min_value=1, max_value=500, value=45)
tx_amount = st.sidebar.slider("Transaction Amount ($)", min_value=100.0, max_value=100000.0, value=49500.0, step=500.0)
simulate_btn = st.sidebar.button("🚀 Ingest & Run Multi-Agent Investigation")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Active Monitoring Nodes", value="500 Accounts", delta="+12 today")
with col2:
    st.metric(label="GNN Model Status", value="Online (GraphSAGE)", delta="Optimal")
with col3:
    st.metric(label="Agent Swarm Status", value="Ready (LangGraph)", delta="3 Agents Active")

st.markdown("### 📊 Live Transaction & Forensic Triage Stream")

if simulate_btn:
    with st.spinner("Streaming transaction through FastAPI & triggering LangGraph agent swarm..."):
        payload = {
            "tx_id": int(time.time()),
            "source_node": int(target_node),
            "target_node": 112,
            "amount": float(tx_amount),
            "timestamp": int(time.time())
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/api/v1/ingest", json=payload)
            res_data = response.json()
            
            risk = res_data.get("risk_score", 0.0)
            is_threat = res_data.get("threat_detected", False)
            dossier = res_data.get("forensic_dossier")
            
            if is_threat:
                st.error(f"🚨 CRITICAL THREAT DETECTED! Risk Score: {risk:.4f}")
            else:
                st.success(f"✅ Transaction Clean. Risk Score: {risk:.4f}")
                
            if dossier:
                st.markdown("---")
                st.subheader("📋 Autonomous Executive Forensic Dossier")
                
                d1, d2 = st.columns(2)
                with d1:
                    st.info(f"**Target Account:** #{dossier['target_node']}")
                    st.info(f"**Compliance Flags:** {', '.join(dossier['compliance_flags'])}")
                with d2:
                    st.warning(f"**Verdict:** {dossier['verdict']}")
                    st.error(f"**Action Required:** {dossier['action']}")
                    
                st.markdown("### 🕵️ Agent Investigation Trace Logs")
                for log in dossier["logs"]:
                    st.code(log, language="text")
            else:
                st.info("No threat threshold breached. Transaction passed standard filters.")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection refused! Ensure your FastAPI server is running (`python main_step3.py`).")