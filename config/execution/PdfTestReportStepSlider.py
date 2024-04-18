import os
import re
import datetime
from typing import Literal
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import KeepTogether
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from libraries.test_paths import TestsOutputPath, TestsReportsPath, TestsSeleniumScreenShootsPath

class PdfTestReportStepSlider:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        """Inicializar el listener de reporte de pasos con imágenes.
        
        Se inicializan las variables necesarias para el listener.
        
        variables:
        - keyword_config: (bool) Indica si el keyword es de configuración. Esto es para separar los keywords de configuración de los keywords de datos porque se agrega la evidencia tomada de la configuracion (SETUP, TEARDOWN) a todas las pruebas.
        - keywords_config: (list) Lista de keywords de configuración.
        - current_test: (dict) Diccionario con el nombre del test actual.
        - screenshot_element_counter: (int) Contador de capturas de pantalla de elementos.
        - screenshot_counter: (int) Contador de capturas de pantalla.
        - base_path: (str) Ruta base del proyecto.
        - reports_path: (str) Ruta de los reportes.
        """
        self.color_scheme = {
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
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'Custom',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            textColor=colors.black,  
            alignment=1  
        )
        self.keyword_config = False
        self.keywords_config = []
        self.current_test = {}
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.base_path = TestsOutputPath().path()
        self.reports_path = TestsReportsPath().path()
        self.selenium_screenshots_path = TestsSeleniumScreenShootsPath().path()

    def start_test(self, name, attrs):
        """Iniciar un test.

        Se eliminan las capturas de pantalla anteriores y se inicializan las variables necesarias para el test.
        """
        self.current_test = {
            'name': name
        }
        self.story = []

    def end_test(self, name, attrs):
        """Finalizar un test.

        Se genera el reporte de pasos con imágenes y se reinician las variables necesarias para el siguiente test.
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = self.current_test["name"] + " " + today.replace(":", "-")
        path_to_report = os.path.abspath(os.path.join(self.reports_path, test_name))

        if not os.path.exists(path_to_report):
            os.mkdir(path_to_report)
        
        if not os.path.exists(os.path.join(path_to_report, "report_pdf_slider")):
            os.mkdir(os.path.join(path_to_report, "report_pdf_slider"))

        doc = SimpleDocTemplate(os.path.join(path_to_report, "report_pdf_slider", self.current_test["name"]  + ".pdf"), pagesize=letter)

        title_style = ParagraphStyle(
            'TitleCustom',
            parent=self.styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.black,
            alignment=1
        )

        date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.black,
            alignment=2
        )

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
            [Paragraph("Nombre del Test", self.custom_style), Paragraph(self.current_test["name"], self.custom_style)],
            [Paragraph("Estado", self.custom_style), Paragraph(attrs["status"], self.custom_style)]
        ]
        toc_table = Table(toc_data, colWidths=[3.5 * inch, 3.5 * inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.color_scheme["info_color"]),
            ('BACKGROUND', (0, 1), (0, 1), self.color_scheme["info_color"]),
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
        doc.build(custom_story + self.keywords_config + self.story)

        self.story = []
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1
        self.__clear_screenshots_folder()

    def start_keyword(self, name, attrs):
        """Iniciar un keyword.

        Se verifica si el keyword es de configuración y se agrega a la lista de keywords de configuración.
        """
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        """Finalizar un keyword.

        Se verifica si el keyword es de configuración y se agrega a la lista de keywords de configuración.
        """
        step_image = re.search(
            r"STEP:IMAGE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            "===>".join(attrs['tags'])
        )
        step_capture_selenium = re.search(
            r"STEP:CAPTURE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            "===>".join(attrs['tags'])
        )
        step_element_selenium = re.search(
            r"STEP:ELEMENT:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            "===>".join(attrs['tags'])
        )

        if step_image:
            image_path = self.__take_screenshot()
            step_re_data = step_image
        
        if step_capture_selenium:
            image_path = self.__get_image_content("selenium-screenshot-", self.screenshot_counter)
            self.screenshot_counter += 1
            step_re_data = step_capture_selenium
        
        if step_element_selenium:
            image_path = self.__get_image_content("selenium-element-screenshot-", self.screenshot_element_counter)
            self.screenshot_element_counter += 1
            step_re_data = step_element_selenium

        if any([step_image, step_capture_selenium, step_element_selenium]):
            step_title = step_re_data.group(1)

            if self.keyword_config:
                
                
                
                img = Image(image_path)
                img.drawHeight = 3.5 * inch
                img.drawWidth = 6.5 * inch
                step_content = KeepTogether([Paragraph(step_title, self.custom_style), Spacer(1, 0.25 * inch), img, Spacer(1, 0.25 * inch)])
                self.keywords_config.append(step_content)
            else:
                img = Image(image_path)
                img.drawHeight = 3.5 * inch
                img.drawWidth = 6.5 * inch
                step_content = KeepTogether([Paragraph(step_title, self.custom_style), Spacer(1, 0.25 * inch), img, Spacer(1, 0.25 * inch)])
                
                
                
                self.story.append(step_content)
        
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = False

    def log_message(self, message):
        """Log de un mensaje.

        Se verifica si el mensaje tiene un título y se agrega a la lista de keywords.
        """
        step_image = re.search(
            r"STEP:IMAGE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            message['message']
        )
        step_capture_selenium = re.search(
            r"STEP:CAPTURE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            message['message']
        )
        step_element_selenium = re.search(
            r"STEP:ELEMENT:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            message['message']
        )

        if step_image:
            image_path = self.__take_screenshot()
            step_re_data = step_image
        
        if step_capture_selenium:
            image_path = self.__get_image_content("selenium-screenshot-", self.screenshot_counter)
            self.screenshot_counter += 1
            step_re_data = step_capture_selenium
        
        if step_element_selenium:
            image_path = self.__get_image_content("selenium-element-screenshot-", self.screenshot_element_counter)
            self.screenshot_element_counter += 1
            step_re_data = step_element_selenium

        if any([step_image, step_capture_selenium, step_element_selenium]):
            step_title = step_re_data.group(1)

            if self.keyword_config:
                
                
                
                img = Image(image_path)
                img.drawHeight = 3.5 * inch
                img.drawWidth = 6.5 * inch
                step_content = KeepTogether([Paragraph(step_title, self.custom_style), Spacer(1, 0.25 * inch), img, Spacer(1, 0.25 * inch)])
                self.keywords_config.append(step_content)
            else:
                img = Image(image_path)
                img.drawHeight = 3.5 * inch
                img.drawWidth = 6.5 * inch
                step_content = KeepTogether([Paragraph(step_title, self.custom_style), Spacer(1, 0.25 * inch), img, Spacer(1, 0.25 * inch)])
                
                
                
                self.story.append(step_content)

    def __get_image_content(self, type_image: Literal["selenium-element-screenshot-", "selenium-screenshot-"], counter: int):
        image_path = os.path.join(self.selenium_screenshots_path, type_image + str(counter) + ".png")
        return image_path

    def __take_screenshot(self):
        image_path = os.path.join(self.selenium_screenshots_path,"imagen.png")
        im1 = ImageGrab.grab()
        im1.save(image_path)
        return image_path
    
    def __clear_screenshots_folder(self):
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

        if os.path.exists(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot")):
            for file in os.listdir(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot")):
                os.remove(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot", file))

    def end_suite(self, name, attrs):
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))