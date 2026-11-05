import csv
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

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

    def export_sar_pdf(self, dossier: dict) -> str:
        """
        Generates an official, highly styled PDF Suspicious Activity Report (SAR) for compliance officers.
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab is not installed. Run `pip install reportlab`.")
        
        target_node = dossier.get("target_node", "unknown")
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"SAR_Executive_Report_Node_{target_node}_{timestamp_str}.pdf")
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1A202C'),
            spaceAfter=10
        )
        
        story.append(Paragraph("🛡️ OMNI-SENTINEL: Suspicious Activity Report (SAR)", title_style))
        story.append(Paragraph(f"<b>Generated Timestamp:</b> {datetime.now().isoformat()}", styles['Normal']))
        story.append(Spacer(1, 15))
        
        data = [
            ["Target Account", f"#{target_node}"],
            ["Risk Score", f"{dossier.get('risk_score', 0.0):.4f}"],
            ["Compliance Flags", ", ".join(dossier.get("compliance_flags", []))],
            ["Verdict", dossier.get("verdict", "N/A")],
            ["Recommended Action", dossier.get("action", "N/A")]
        ]
        
        t = Table(data, colWidths=[140, 360])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#EDF2F7')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2D3748')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0'))
        ]))
        story.append(t)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("<b>Agent Investigation Trace Logs:</b>", styles['Heading2']))
        story.append(Spacer(1, 6))
        for log in dossier.get("logs", []):
            story.append(Paragraph(f"• {log}", styles['Normal']))
            story.append(Spacer(1, 4))
            
        doc.build(story)
        print(f"✅ PDF Compliance Report successfully generated at: {filename}")
        return filename