from engine.agent_swarm import OmniSentinelSwarm

def run_step2_agent_pipeline():
    print("🤖 [Step 2] Initializing Omni-Sentinel Multi-Agent Forensic Swarm (LangGraph)...")
    swarm = OmniSentinelSwarm()
    
    # Simulate a high-risk node flagged by our GNN model in Step 1
    target_node_id = 45
    simulated_gnn_score = 0.9421
    
    print(f"🚨 [Alert Triggered] GNN flagged Node #{target_node_id} with Anomaly Score: {simulated_gnn_score:.4f}")
    print("🔄 [Swarm Dispatch] Handing over investigation to LangGraph Multi-Agent Swarm...\n")
    
    result = swarm.run_investigation(node_id=target_node_id, risk_score=simulated_gnn_score)
    
    print("=" * 60)
    print("📋 OMNI-SENTINEL AUTOMATED FORENSIC DOSSIER")
    print("=" * 60)
    print(f"Target Account ID : #{result['node_id']}")
    print(f"GNN Risk Score    : {result['risk_score']:.4f}")
    print(f"Compliance Flags  : {', '.join(result['compliance_flags'])}")
    print(f"Final Verdict     : {result['final_verdict']}")
    print(f"Recommended Action: {result['action_recommended']}")
    print("-" * 60)
    print("🕵️ Agent Investigation Trace Logs:")
    for log in result["investigation_logs"]:
        print(f"   {log}")
    print("=" * 60)

if __name__ == "__main__":
    run_step2_agent_pipeline()