import os
import re
from typing import Literal
import datetime
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageGrab
import base64
import io
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from libraries.test_paths import TestsOutputPath, TestsReportsPath, TestsSeleniumScreenShootsPath

class HtmlTestReportStepHorizontalSlider:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        """Inicializar el listener de reporte de pasos con imágenes.
        
        Se inicializan las variables necesarias para el listener.
        
        Variables:
        - keyword_config: (bool) Indica si el keyword es de configuración. Esto es para separar los keywords de configuración de los keywords de datos porque se agrega la evidencia tomada de la configuracion (SETUP, TEARDOWN) a todas las pruebas.
        - keywords_config: (list) Lista de keywords de configuración.
        - keywords_data: (list) Lista de keywords de datos.
        - current_test: (dict) Diccionario con el nombre del test actual.
        - screenshot_element_counter: (int) Contador de capturas de pantalla de elementos.
        - screenshot_counter: (int) Contador de capturas de pantalla.
        - base_path: (str) Ruta base del proyecto.
        - reports_path: (str) Ruta de los reportes.
        - selenium_screenshots_path: (str) Ruta de las capturas de pantalla de Selenium.
        """
        self.keyword_config = False
        self.keywords_config = []
        self.keywords_data = []
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
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

        self.current_test = {
            'name': name
        }

    def end_test(self, name, attrs):
        """Finalizar un test.

        Se genera el reporte de pasos con imágenes y se reinician las variables necesarias para el siguiente test.
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = self.current_test["name"] + " " + today.replace(":", "-")
        path_to_report = os.path.abspath(os.path.join(self.reports_path, test_name))

        if not os.path.exists(path_to_report):
            os.mkdir(path_to_report)

        path_to_report = os.path.join(path_to_report, "report_horizontal_step_slider")
        os.mkdir(path_to_report)

        env = Environment(loader=FileSystemLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "static", 'templates'))
            )
        )
        template = env.get_template('step_horizontal_slider_report.html')
        output = template.render(testname=self.current_test["name"], steps_data=self.keywords_config + self.keywords_data, status=attrs['status'].lower())
        with open(os.path.join(path_to_report, self.current_test["name"] + ".html"), "w", encoding="utf-8") as f:
            f.write(output)

        self.keywords_data = []
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1

    def start_keyword(self, name, attrs):
        """Iniciar un keyword.

        Se verifica si el keyword es de configuración y se inicializa la variable para agregar la evidencia a los keywords de configuración.
        """
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        """Finalizar un keyword.

        Se verifica si el keyword es de configuración y se reinicia la variable para agregar la evidencia a los keywords de datos.
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
            image_content = self.__take_screenshot()
            step_re_data = step_image
        
        if step_capture_selenium:
            image_content = self.__get_image_content("selenium-screenshot-", self.screenshot_counter)
            self.screenshot_counter += 1
            step_re_data = step_capture_selenium
        
        if step_element_selenium:
            image_content = self.__get_image_content("selenium-element-screenshot-", self.screenshot_element_counter)
            self.screenshot_element_counter += 1
            step_re_data = step_element_selenium

        if any([step_image, step_capture_selenium, step_element_selenium]):
            step_data = {}
            level = step_re_data.group(2) if step_re_data.group(2) else "INFO"
            step_title = step_re_data.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title
            step_data["step_image"] = image_content

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)
        
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = False

    def log_message(self, message):
        """Log de un mensaje.

        Se verifica si el mensaje contiene un tag de imagen y se agrega la imagen al reporte.
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
            image_content = self.__take_screenshot()
            step_re_data = step_image
        
        if step_capture_selenium:
            image_content = self.__get_image_content("selenium-screenshot-", self.screenshot_counter)
            self.screenshot_counter += 1
            step_re_data = step_capture_selenium
        
        if step_element_selenium:
            image_content = self.__get_image_content("selenium-element-screenshot-", self.screenshot_element_counter)
            self.screenshot_element_counter += 1
            step_re_data = step_element_selenium

        if any([step_image, step_capture_selenium, step_element_selenium]):
            step_data = {}
            level = step_re_data.group(2) if step_re_data.group(2) else "INFO"
            step_title = step_re_data.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title
            step_data["step_image"] = image_content

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)

    def __get_image_content(self, type_image: Literal["selenium-element-screenshot-", "selenium-screenshot-"], counter: int):
        image_path = os.path.join(self.selenium_screenshots_path, type_image + str(counter) + ".png")
        im = Image.open(image_path)
        buff = io.BytesIO()
        im.save(buff, format="PNG")
        return base64.b64encode(buff.getvalue()).decode("utf-8")

    def __take_screenshot(self):
        image_path = os.path.join(self.reports_path,"imagen.png")

        im1 = ImageGrab.grab()
        im1.save(image_path)

        im = Image.open(image_path)
        buff = io.BytesIO()
        im.save(buff, format="PNG")
        os.remove(image_path)

        return base64.b64encode(buff.getvalue()).decode("utf-8")
