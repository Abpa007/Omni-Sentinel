import operator
from typing import Annotated, Dict, List, TypedDict, Any
from langgraph.graph import StateGraph, END

# Define the shared state structure for the multi-agent investigation
class InvestigationState(TypedDict):
    node_id: int
    risk_score: float
    graph_topology_summary: Dict[str, Any]
    investigation_logs: Annotated[List[str], operator.add]
    compliance_flags: List[str]
    final_verdict: str
    action_recommended: str


class OmniSentinelSwarm:
    def __init__(self):
        self.workflow = self._build_workflow()

    def _graph_explorer_node(self, state: InvestigationState) -> InvestigationState:
        node_id = state["node_id"]
        # Simulate querying Neo4j / Graph database for neighborhood topology
        log = f"[Graph Explorer Agent] Queried 2-hop neighborhood for Node #{node_id}. Detected 3 connected accounts, 1 circular loop pattern."
        
        topology = {
            "degree_centrality": 0.85,
            "connected_shell_companies": 2,
            "total_ring_volume": 49500.0
        }
        
        return {
            "graph_topology_summary": topology,
            "investigation_logs": [log]
        }

    def _risk_auditor_node(self, state: InvestigationState) -> InvestigationState:
        score = state["risk_score"]
        topology = state["graph_topology_summary"]
        
        flags = []
        if score > 0.8:
            flags.append("HIGH_PROBABILITY_MONEY_LAUNDERING_RING")
        if topology["connected_shell_companies"] > 0:
            flags.append("SHELL_COMPANY_CLUSTER_ASSOCIATION")
            
        log = f"[Risk Auditor Agent] Evaluated risk score ({score}) and topology metrics. Identified compliance flags: {flags}"
        
        return {
            "compliance_flags": flags,
            "investigation_logs": [log]
        }

    def _synthesizer_node(self, state: InvestigationState) -> InvestigationState:
        node_id = state["node_id"]
        flags = state["compliance_flags"]
        score = state["risk_score"]
        
        if "HIGH_PROBABILITY_MONEY_LAUNDERING_RING" in flags:
            verdict = "CRITICAL THREAT: Active Syndicate Participation Confirmed"
            action = "Freeze account assets immediately and file Suspicious Activity Report (SAR)."
        else:
            verdict = "MONITORED: Elevated risk profile requiring human review."
            action = "Place account under enhanced transactional surveillance."

        log = f"[Lead Forensic Synthesizer] Compiled final executive dossier for Node #{node_id} with risk level {score:.2f}."
        
        return {
            "final_verdict": verdict,
            "action_recommended": action,
            "investigation_logs": [log]
        }

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(InvestigationState)

        # Add agent nodes
        workflow.add_node("graph_explorer", self._graph_explorer_node)
        workflow.add_node("risk_auditor", self._risk_auditor_node)
        workflow.add_node("synthesizer", self._synthesizer_node)

        # Define deterministic agent investigation sequence
        workflow.set_entry_point("graph_explorer")
        workflow.add_edge("graph_explorer", "risk_auditor")
        workflow.add_edge("risk_auditor", "synthesizer")
        workflow.add_edge("synthesizer", END)

        return workflow.compile()

    def run_investigation(self, node_id: int, risk_score: float) -> Dict[str, Any]:
        initial_state = {
            "node_id": node_id,
            "risk_score": risk_score,
            "graph_topology_summary": {},
            "investigation_logs": [],
            "compliance_flags": [],
            "final_verdict": "",
            "action_recommended": ""
        }
        return self.workflow.invoke(initial_state)