"""
En este listener es posible generar un reporte de los pasos de ejecución de un test case. Para agregar un paso al reporte, se debe agregar el tag STEP: en la keyword o en el mensaje de log. El mensaje se puede usar para reportar información adicional de un paso, como por ejemplo, el valor de una variable, el resultado de una operación, etc.

El reporte se genera en la carpeta output/reports/report_step_log/ y se genera un archivo PDF por cada test que se ejecute.

Para utilizar el listener, se debe especificar como listener al ejecutar las pruebas:
- robot --listener PdfTestStepLogReport.py tests

Ejemplo:
    *** Keywords ***
    My Keyword
        [Tags]  STEP:DESCRIPCIÓN DEL PASO:INFO
        No Operation

    My Other Keyword
        [Tags]  STEP:DESCRIPCIÓN DEL PASO 2
        No Operation

    My Other Keyword
        [Tags]  STEP:DESCRIPCIÓN DEL PASO 3:FAIL
        No Operation

Los estatus posibles son:
- INFO
- PASS
- CRITICAL
- FAIL
- FALTA
- WARNING
- DEBUG

El valor predeterminado es INFO.

También es posible utilizar la keyword Log con la misma estructura de tags.

Consideraciones:
- Si bien se puede usar STEP: para definir un paso también se tomara en cuenta STEP:IMAGE: para agregar un paso en este reporte pero no tomara la captura de pantalla, esto con el fin de poder reutilizar la misma descripción de paso en diferentes reportes.
"""
import os
import re
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from test_paths import TestsOutputPath, TestsReportsPath

class PdfTestStepLogReport:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.keyword_config = False
        self.keywords_config = []
        self.current_test = {}
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.base_path = TestsOutputPath().path()
        self.reports_path = TestsReportsPath().path()
        self.styles = getSampleStyleSheet()

    def start_test(self, name, attrs):
        self.current_test = {
            'name': name
        }
        self.story = []

    def end_test(self, name, attrs):
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = self.current_test["name"] + " " + today.replace(":", "-")
        path_to_report = os.path.abspath(os.path.join(self.reports_path, test_name))

        if not os.path.exists(path_to_report):
            os.mkdir(path_to_report)

        if not os.path.exists(os.path.join(path_to_report, "report_pdf_log")):
            os.mkdir(os.path.join(path_to_report, "report_pdf_log"))

        doc = SimpleDocTemplate(os.path.join(path_to_report, "report_pdf_log", self.current_test["name"] + ".pdf"), pagesize=letter)
        doc.build(self.keywords_config + self.story)
        self.story = []

    def start_keyword(self, name, attrs):
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        tag_message_title = re.search(
            r"^STEP:(?:IMAGE:)?(?:CAPTURE:)?(?:ELEMENT:)?(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            "===>".join(attrs['tags'])
        )

        if tag_message_title:
            step_title = tag_message_title.group(1)
            
            if self.keyword_config:
                titulo = Paragraph(step_title, self.styles['Heading1'])
                self.keywords_config.append(titulo)
            else:
                titulo = Paragraph(step_title, self.styles['Heading1'])
                self.story.append(titulo)
        
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = False

    def log_message(self, message):
        tag_message_title = re.search(
            r"^STEP:(?:IMAGE:)?(?:CAPTURE:)?(?:ELEMENT:)?(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            message['message']
        )

        if tag_message_title:
            step_title = tag_message_title.group(1)

            if self.keyword_config:
                titulo = Paragraph(step_title, self.styles['Heading1'])
                self.keywords_config.append(titulo)
            else:
                titulo = Paragraph(step_title, self.styles['Heading1'])
                self.story.append(titulo)
