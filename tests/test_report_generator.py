import os
import pytest
from engine.report_generator import ComplianceReportGenerator

def test_compliance_report_generation():
    generator = ComplianceReportGenerator(output_dir="./test_reports")
    
    sample_dossier = {
        "target_node": 999,
        "risk_score": 0.95,
        "compliance_flags": ["SHELL_COMPANY_CLUSTER", "HIGH_RISK_VELOCITY"],
        "verdict": "CRITICAL THREAT: Money Laundering Confirmed",
        "action": "Freeze account and file SAR immediately.",
        "logs": [
            "[Graph Explorer] Found 5 connected nodes.",
            "[Risk Auditor] Assigned high risk score 0.95.",
            "[Lead Synthesizer] Compiled final dossier."
        ]
    }
    
    # Test JSON export
    json_path = generator.export_executive_summary_json(sample_dossier)
    assert os.path.exists(json_path)
    
    # Test CSV export
    csv_path = generator.export_sar_csv([sample_dossier])
    assert os.path.exists(csv_path)
    
    # Test PDF export
    pdf_path = generator.export_sar_pdf(sample_dossier)
    assert os.path.exists(pdf_path)
    
    # Cleanup generated test files
    for p in [json_path, csv_path, pdf_path]:
        if os.path.exists(p):
            os.remove(p)
    if os.path.exists("./test_reports"):
        try:
            os.rmdir("./test_reports")
        except OSError:
            pass