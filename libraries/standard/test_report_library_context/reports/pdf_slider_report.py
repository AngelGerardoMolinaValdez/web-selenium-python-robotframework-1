import os
import base64
from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import KeepTogether
from test_report_library_context.reports.base_report import BaseReport

class PdfSliderReport(BaseReport):
    def create(self, test_name, status, steps, setup_steps, teardown_steps, base_path):
        report_dir = os.path.join(base_path, "pdf_slider")
        report_name = test_name + ".pdf"
        report_path = os.path.join(report_dir, report_name)

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        color_scheme = {
            "background_color": colors.HexColor("#333"),
            "container_background_color": colors.HexColor("#454545"),
            "text_color": colors.HexColor("#eaeaea"),
            "info_color": colors.HexColor("#17a2b8"),
            "debug_color": colors.HexColor("#6c757d"),
            "pass_color": colors.HexColor("#28a745"),
            "fail_color": colors.HexColor("#dc3545"),
            "fatal_color": colors.HexColor("#870000"),
            "critical_color": colors.HexColor("#ff5733"),
            "warning_color": colors.HexColor("#ff851b")
        }
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            textColor=colors.black,  
            alignment=1  
        )
        title_style = ParagraphStyle(
            'TitleCustom',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.black,
            alignment=1
        )
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.black,
            alignment=2
        )

        doc = SimpleDocTemplate(report_path, pagesize=letter)

        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        date_paragraph = Paragraph("Fecha: " + current_date, date_style)
        custom_story = []
        custom_story.append(date_paragraph)
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Paragraph("Reporte de Ejecución Automatizada", title_style))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        toc_data = [
            [Paragraph("Nombre del Test", custom_style), Paragraph(test_name, custom_style)],
            [Paragraph("Estatus", custom_style), Paragraph(status, custom_style)]
        ]
        toc_table = Table(toc_data, colWidths=[3.5 * inch, 3.5 * inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), color_scheme["info_color"]),
            ('BACKGROUND', (0, 1), (0, 1), color_scheme["info_color"]),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('TEXTTRANSFORM', (0, 0), (-1, -1), 'UPPERCASE'),
            ('BOX', (0,0), (-1,-1), 1, colors.black),  
            ('GRID', (0,0), (-1,-1), 1, colors.black),  
        ]))
        custom_story.append(toc_table)
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))

        steps_data = setup_steps + steps + teardown_steps
        content = []
        for step_info in steps_data:
            image_data = base64.b64decode(step_info["screenshot"])
            image = BytesIO(image_data)
            img = Image(image)
            img.drawHeight = 3.5 * inch
            img.drawWidth = 6.5 * inch
            step_content = KeepTogether([Paragraph(step_info["title"], custom_style), Spacer(1, 0.25 * inch), img, Spacer(1, 0.25 * inch)])
            content.append(step_content)

        doc.build(custom_story + content)
