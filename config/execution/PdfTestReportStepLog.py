import os
import re
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from libraries.test_paths import TestsOutputPath, TestsReportsPath

class PdfTestReportStepLog:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        """Inicializar el listener de reporte de pasos con imágenes.
        
        Se inicializan las variables necesarias para el listener.
        
        Variables:
        - keyword_config: (bool) Indica si el keyword es de configuración. Esto es para separar los keywords de configuración de los keywords de datos porque se agrega la evidencia tomada de la configuracion (SETUP, TEARDOWN) a todas las pruebas.
        - keywords_config: (list) Lista de keywords de configuración.
        - current_test: (dict) Diccionario con el nombre del test actual.
        - base_path: (str) Ruta base del proyecto.
        - reports_path: (str) Ruta de los reportes.
        """
        self.keyword_config = False
        self.keywords_config = []
        self.current_test = {}
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.base_path = TestsOutputPath().path()
        self.reports_path = TestsReportsPath().path()
        self.styles = getSampleStyleSheet()

    def start_test(self, name, attrs):
        """Iniciar un test.

        Se inicializan las variables necesarias para el test.
        """
        self.current_test = {
            'name': name
        }
        self.story = []

    def end_test(self, name, attrs):
        """Finalizar un test.

        Se genera el reporte de pasos y se reinician las variables necesarias para el siguiente test.
        """
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
        """Iniciar un keyword.

        Se verifica si el keyword es de configuración y se agrega a la lista de keywords de configuración.
        """
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        """Finalizar un keyword.

        Se verifica si el keyword es de configuración y se agrega a la lista de keywords de configuración.
        """
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
        """Log de un mensaje.

        Se verifica si el mensaje tiene un título y se agrega a la lista de keywords.
        """
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
