import csv
import json
import os
from datetime import datetime

class ComplianceReportGenerator:
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_sar_csv(self, dossier_list: list) -> str:
        """
        Exports a batch of forensic dossiers into a regulatory-compliant CSV file format.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"SAR_Compliance_Report_{timestamp_str}.csv")
        
        fieldnames = ["target_node", "risk_score", "verdict", "action", "compliance_flags", "timestamp"]
        
        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for dossier in dossier_list:
                writer.writerow({
                    "target_node": dossier.get("target_node"),
                    "risk_score": dossier.get("risk_score"),
                    "verdict": dossier.get("verdict"),
                    "action": dossier.get("action"),
                    "compliance_flags": ", ".join(dossier.get("compliance_flags", [])),
                    "timestamp": datetime.now().isoformat()
                })
        
        print(f"✅ SAR Compliance CSV report successfully generated at: {filename}")
        return filename

    def export_executive_summary_json(self, dossier: dict) -> str:
        """
        Exports an individual forensic dossier as an official JSON audit package.
        """
        target_node = dossier.get("target_node", "unknown")
        filename = os.path.join(self.output_dir, f"SAR_Dossier_Node_{target_node}.json")
        
        with open(filename, mode="w", encoding="utf-8") as json_file:
            json.dump(dossier, json_file, indent=4)
            
        print(f"✅ Executive SAR JSON dossier saved at: {filename}")
        return filename