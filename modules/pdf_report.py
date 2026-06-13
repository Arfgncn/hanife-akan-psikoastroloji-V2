def make_pdf(title, content):
    """
    Türkçe karakter ve uzun satır sorunlarını azaltan güvenli PDF üretici.
    Önce ReportLab kullanır; yoksa FPDF ile sade çıktı verir.
    """
    try:
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        normal = ParagraphStyle("TRNormal", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14)
        heading = ParagraphStyle("TRHeading", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20)

        story = [Paragraph(str(title).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), heading), Spacer(1, 12)]
        for line in str(content).splitlines():
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe if safe.strip() else "&nbsp;", normal))
            story.append(Spacer(1, 4))
        doc.build(story)
        return buffer.getvalue()
    except Exception:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 8, str(title).encode("latin-1", "replace").decode("latin-1"))
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)
        for p in str(content).splitlines():
            safe = p.encode("latin-1", "replace").decode("latin-1")
            words = []
            for w in safe.split(" "):
                if len(w) > 55:
                    words.extend([w[i:i+55] for i in range(0, len(w), 55)])
                else:
                    words.append(w)
            pdf.multi_cell(0, 6, " ".join(words))
        return pdf.output(dest="S").encode("latin-1")
