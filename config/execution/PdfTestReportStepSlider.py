import os
import re
import datetime
from typing import Literal
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
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
        self.keyword_config = False
        self.keywords_config = []
        self.current_test = {}
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.base_path = TestsOutputPath().path()
        self.reports_path = TestsReportsPath().path()
        self.selenium_screenshots_path = TestsSeleniumScreenShootsPath().path()
        self.styles = getSampleStyleSheet()

    def start_test(self, name, attrs):
        """Iniciar un test.

        Se eliminan las capturas de pantalla anteriores y se inicializan las variables necesarias para el test.
        """
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

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
        doc.build(self.keywords_config + self.story)

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
                self.keywords_config.append(Paragraph(step_title, self.styles['Heading1']))
                self.keywords_config.append(Spacer(1, 12))
                self.keywords_config.append(Image(image_path, 7*inch, 5*inch))
            else:
                self.story.append(Paragraph(step_title, self.styles['Heading1']))
                self.story.append(Spacer(1, 12))
                self.story.append(Image(image_path, 7*inch, 5*inch))
        
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
                self.keywords_config.append(Paragraph(step_title, self.styles['Heading1']))
                self.keywords_config.append(Spacer(1, 12))
                self.keywords_config.append(Image(image_path, 7*inch, 5*inch))
            else:
                self.story.append(Paragraph(step_title, self.styles['Heading1']))
                self.story.append(Spacer(1, 12))
                self.story.append(Image(image_path, 7*inch, 5*inch))

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
