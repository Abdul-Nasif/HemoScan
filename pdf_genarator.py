from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import os

def generate_medical_report(patient_id, name, age, gender,
                            hb, mch, mchc, mcv,
                            prediction, risk, anemia_type):

    os.makedirs("reports", exist_ok=True)

    file_path = f"reports/{patient_id}_report.pdf"

    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("HemoScan AI – Anemia Screening Report", styles['Title']))
    elements.append(Spacer(1, 20))

    # Patient Info
    patient_data = [
        ["Patient ID", patient_id],
        ["Name", name],
        ["Age", age],
        ["Gender", gender]
    ]

    elements.append(Paragraph("Patient Information", styles['Heading2']))
    elements.append(Table(patient_data))
    elements.append(Spacer(1, 20))

    # CBC Values
    cbc_data = [
        ["Parameter", "Value", "Normal Range"],
        ["Hemoglobin", hb, "12–16 g/dL"],
        ["MCH", mch, "27–33 pg"],
        ["MCHC", mchc, "32–36 g/dL"],
        ["MCV", mcv, "80–100 fL"]
    ]

    elements.append(Paragraph("CBC Test Results", styles['Heading2']))
    elements.append(Table(cbc_data))
    elements.append(Spacer(1, 20))

    # Model Prediction
    prediction_data = [
        ["Prediction", prediction],
        ["Risk Level", risk],
        ["Anemia Type", anemia_type]
    ]

    elements.append(Paragraph("AI Analysis", styles['Heading2']))
    elements.append(Table(prediction_data))
    elements.append(Spacer(1, 20))

    # Add Graph Images
    elements.append(Paragraph("Visual Analysis", styles['Heading2']))

    graph_files = [
        "reports/cbc_comparison_chart.png",
        "reports/hemoglobin_risk_indicator.png",
        "reports/cbc_radar_chart.png"
    ]

    for graph in graph_files:
        if os.path.exists(graph):
            elements.append(Image(graph, width=5*inch, height=3*inch))
            elements.append(Spacer(1, 10))

    # Information about anemia
    elements.append(Paragraph("About Anemia", styles['Heading2']))

    anemia_info = """
    Anemia is a medical condition where the body does not have enough healthy
    red blood cells or hemoglobin to carry adequate oxygen to tissues.
    
    Common causes include:
    • Iron deficiency
    • Vitamin B12 deficiency
    • Chronic diseases
    • Blood loss
    
    Early detection through Complete Blood Count (CBC) analysis helps prevent
    complications such as fatigue, weakness, and cardiovascular stress.
    """

    elements.append(Paragraph(anemia_info, styles['BodyText']))

    # Build PDF
    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    pdf.build(elements)

    print("Report saved:", file_path)