import streamlit as st
import requests
import json
import time
import os
from engine.report_generator import ComplianceReportGenerator

st.set_page_config(
    page_title="Omni-Sentinel | Financial Forensics Command Center",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Report Generator
report_gen = ComplianceReportGenerator(output_dir="./reports")

st.title("🛡️ Omni-Sentinel: Autonomous Financial Forensics & Threat Intelligence Mesh")
st.markdown("---")

# Navigation Tabs
tab_live, tab_analytics = st.tabs(["🚀 Live Investigation Triage", "📊 Compliance & SAR Audit Reports"])

with tab_live:
    # Sidebar Controls for Live Triage
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
                        
                    # Auto-generate downloadable SAR report package
                    try:
                        pdf_path = report_gen.export_sar_pdf(dossier)
                        csv_path = report_gen.export_sar_csv([dossier])
                        st.success(f"📁 SAR Compliance files generated successfully!")
                    except Exception as report_err:
                        st.warning(f"Could not auto-generate report files: {report_err}")
                else:
                    st.info("No threat threshold breached. Transaction passed standard filters.")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection refused! Ensure your FastAPI server is running (`python main_step3.py`).")

    st.markdown("---")
    st.subheader("🔌 Real-Time WebSocket Telemetry Gateway Status")
    st.info("The FastAPI backend is broadcasting live security events on `ws://127.0.0.1:8000/ws/telemetry`. All high-risk triage triggers are pushed instantly across the network mesh.")

with tab_analytics:
    st.subheader("📈 Compliance Analytics & Regulatory Report Exports")
    st.markdown("Generate and download certified **Suspicious Activity Reports (SAR)** and batch compliance metrics for regulatory review.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Total Investigated Anomalies", value="38 Accounts", delta="+5 today")
    with col_b:
        st.metric(label="Average Risk Index", value="0.8412", delta="+0.03")
        
    st.markdown("### 📥 Available Audit Files")
    
    reports_dir = "./reports"
    if os.path.exists(reports_dir):
        files = os.listdir(reports_dir)
        if files:
            for f in sorted(files, reverse=True):
                file_path = os.path.join(reports_dir, f)
                file_size = os.path.getsize(file_path) / 1024
                
                col_file1, col_file2 = st.columns([3, 1])
                with col_file1:
                    st.text(f"📄 {f} ({file_size:.1f} KB)")
                with col_file2:
                    with open(file_path, "rb") as file_btn:
                        st.download_button(
                            label="Download",
                            data=file_btn,
                            file_name=f,
                            mime="application/octet-stream",
                            key=f"dl_{f}"
                        )
        else:
            st.info("No audit reports generated yet. Run a high-risk investigation in the Live Triage tab to generate reports.")
    else:
        st.info("Reports directory is currently empty.")