"""
En este listener es posible generar un reporte de pasos con imágenes. Para agregar una imagen a un paso, se debe agregar el tag STEP:IMAGE: en el mensaje. El mensaje se puede usar para reportar información adicional de un paso, como por ejemplo, el valor de una variable, el resultado de una operación, etc.

El reporte se genera en la carpeta output/reports/report_step_slider/ y se genera un archivo PDF por cada test que se ejecute.

Para utilizar el listener, se debe especificar como listener al ejecutar las pruebas:
- robot --listener PdfTestStepSliderReport.py tests

Ejemplo:
    *** Keywords ***
    My Keyword
        [Tags]  STEP:IMAGE:DESCRIPCIÓN DEL PASO:INFO
        No Operation

    My Other Keyword
        [Tags]  STEP:IMAGE:DESCRIPCIÓN DEL PASO 2
        No Operation

    My Other Keyword
        [Tags]  STEP:IMAGE:DESCRIPCIÓN DEL PASO 3:FAIL
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

Este reporte tiene la misma estructura que el HtmlTestStepsReport2.py, pero con la diferencia de que se agrega una imagen a los pasos.
"""
import os
import re
import datetime
from typing import Literal
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from test_paths import TestsOutputPath, TestsReportsPath, TestsSeleniumScreenShootsPath

class PdfTestStepSliderReport:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
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
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

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
        
        if not os.path.exists(os.path.join(path_to_report, "report_pdf_slider")):
            os.mkdir(os.path.join(path_to_report, "report_pdf_slider"))

        doc = SimpleDocTemplate(os.path.join(path_to_report, "report_pdf_slider", self.current_test["name"]  + ".pdf"), pagesize=letter)
        doc.build(self.keywords_config + self.story)

        self.story = []
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1
        self.clear_screenshots_folder()

    def start_keyword(self, name, attrs):
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
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
    
    def clear_screenshots_folder(self):
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

        if os.path.exists(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot")):
            for file in os.listdir(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot")):
                os.remove(os.path.join(self.selenium_screenshots_path, "selenium-element-screenshot", file))
