import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import base64
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reporter.pdf_reporter import PdfReporter
from reporter.base_reporter import BaseReporter

class PdfReporterManager:
    def create_reporter(self, output_dir: str, report_name: str):
        return PdfReporter(output_dir, report_name)

    def save_reporter(self, reporter: BaseReporter, status: str, message: str = ""):
        path_dir_report = self.__create_report_directory(reporter)
        report_path = self.__generate_report_path(reporter, path_dir_report)
        custom_story, paragraph_style, color_scheme = self.__build_report_content(reporter, status, message)
        self.__build_pdf(report_path, custom_story, paragraph_style, color_scheme, reporter.report_data_value())

    def __create_report_directory(self, reporter):
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name_report = reporter.name_value() + " " + today.replace(":", "-")
        path_dir_report = os.path.abspath(os.path.join(reporter.output_dir_value(), test_name_report))
        if not os.path.exists(path_dir_report):
            os.mkdir(path_dir_report)
        return path_dir_report

    def __generate_report_path(self, reporter, path_dir_report):
        report_name = reporter.name_value() + ".pdf"
        return os.path.join(path_dir_report, report_name)

    def __build_report_content(self, reporter, status, message):
        color_scheme = {
            "background_color": colors.HexColor("#f2f2f2"), 
            "container_background_color": colors.HexColor("#e0e0e0"), 
            "text_color": colors.HexColor("#333333"), 
            "info_color": colors.HexColor("#b3cde0"), 
            "pass_color": colors.HexColor("#ccebc5"), 
            "fail_color": colors.HexColor("#fbb4ae"), 
            "debug_color": colors.HexColor("#decbe4"), 
            "error_color": colors.HexColor("#fbb4ae"), 
            "warning_color": colors.HexColor("#fed9a6") 
        }
        
        styles = getSampleStyleSheet()
        paragraph_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12, 
            textColor=colors.black,  
            alignment=1  
        )
        title_style = ParagraphStyle(
            'TitleCustom',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=20, 
            textColor=colors.HexColor("#333333"),
            alignment=1
        )
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            alignment=2
        )
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        date_paragraph = Paragraph("Report Date: " + current_date, date_style)
        custom_story = []
        custom_story.append(date_paragraph)
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Paragraph("Test Automated Report", title_style))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))

        toc_data = [
            [Paragraph("Test Name", paragraph_style), Paragraph(reporter.name_value(), paragraph_style)],
            [Paragraph("Test Status", paragraph_style), Paragraph(status, paragraph_style)],
            [Paragraph("Test Message", paragraph_style), Paragraph(message, paragraph_style)]
        ]
        toc_table = Table(toc_data, colWidths=[3.5 * inch, 3.5 * inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), color_scheme["background_color"]), 
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#333333")), 
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 12), 
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8), 
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bfbfbf")), 
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cccccc")), 
        ]))
        custom_story.append(toc_table)
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))
        custom_story.append(Spacer(1, 0.25 * inch))

        return (custom_story, paragraph_style, color_scheme)

    def __build_pdf(self, report_path, custom_story, paragraph_style, color_scheme, steps_data):
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        content = []

        for step_info in steps_data:
            level = step_info["level"]
            border_color = color_scheme.get(level + "_color", colors.black)

            image_data = base64.b64decode(step_info["image"])
            image = BytesIO(image_data)
            img = Image(image)
            img.drawHeight = 3.3 * inch
            img.drawWidth = 7.5 * inch
            step_title = Paragraph(step_info["message"], paragraph_style)

            step_table = Table(
                [[step_title], [img]],
                colWidths=[7.5 * inch]
            )
            step_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), border_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, border_color),
            ]))

            content.append(step_table)
            content.append(Spacer(1, 0.2 * inch))

        doc.build(custom_story + content)
