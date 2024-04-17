import os
import re
import datetime
from jinja2 import Environment, FileSystemLoader
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from libraries.test_paths import TestsOutputPath, TestsReportsPath

class HtmlTestReportStepLog:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        """Inicializar el listener de reporte de pasos con imágenes.
        
        Se inicializan las variables necesarias para el listener.
        
        Variables:
        - keyword_config: (bool) Indica si el keyword es de configuración. Esto es para separar los keywords de configuración de los keywords de datos porque se agrega la evidencia tomada de la configuracion (SETUP, TEARDOWN) a todas las pruebas.
        - keywords_config: (list) Lista de keywords de configuración.
        - keywords_data: (list) Lista de keywords de datos.
        - current_test: (dict) Diccionario con el nombre del test actual.
        - base_path: (str) Ruta base del proyecto.
        - reports_path: (str) Ruta de los reportes.
        """
        self.keyword_config = False
        self.keywords_config = []
        self.keywords_data = []
        self.current_test = {}
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.base_path = TestsOutputPath().path()
        self.reports_path = TestsReportsPath().path()

    def start_test(self, name, attrs):
        """Iniciar un test.

        Se inicializan las variables necesarias para el test.
        """
        self.current_test = {
            'name': name
        }

    def end_test(self, name, attrs):
        """Finalizar un test.

        Se genera el reporte de pasos y se reinician las variables necesarias para el siguiente test.
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = self.current_test["name"] + " " + today.replace(":", "-")
        path_to_report = os.path.abspath(os.path.join(self.reports_path, test_name))

        if not os.path.exists(path_to_report):
            os.mkdir(path_to_report)

        path_to_report = os.path.join(path_to_report, "report_step_log")
        os.mkdir(path_to_report)

        env = Environment(loader=FileSystemLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "static", 'templates'))
            )
        )
        template = env.get_template('step_log_report.html')
        output = template.render(testname=self.current_test["name"], steps_data=self.keywords_config + self.keywords_data)
        with open(os.path.join(path_to_report, self.current_test["name"] + ".html"), "w", encoding="utf-8") as f:
            f.write(output)

        self.keywords_data = []

    def start_keyword(self, name, attrs):
        """Iniciar un keyword.

        Se verifica si el keyword es de configuración.
        """
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        """Finalizar un keyword.
        
        Se verifica si el keyword tiene un título y se agrega a la lista de keywords.
        """
        tag_message_title = re.search(
            r"^STEP:(?:IMAGE:)?(?:CAPTURE:)?(?:ELEMENT:)?(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            "===>".join(attrs['tags'])
        )

        if tag_message_title:
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)
        
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = False

    def log_message(self, message):
        """Log de mensaje.

        Se verifica si el mensaje tiene un título y se agrega a la lista de keywords.
        """
        tag_message_title = re.search(
            r"^STEP:(?:IMAGE:)?(?:CAPTURE:)?(?:ELEMENT:)?(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)",
            message['message']
        )

        if tag_message_title:
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)
