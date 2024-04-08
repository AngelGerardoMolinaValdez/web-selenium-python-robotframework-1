"""
En este listener es posible generar un reporte de pasos con imágenes. Para agregar una imagen a un paso, se debe agregar el tag STEP:IMAGE: en el mensaje. El mensaje se puede usar para reportar información adicional de un paso, como por ejemplo, el valor de una variable, el resultado de una operación, etc.

El reporte se genera en la carpeta output/reports/report_step_slider/ y se genera un archivo HTML por cada test que se ejecute.

Para utilizar el listener, se debe especificar como listener al ejecutar las pruebas:
- robot --listener HtmlTestStepSliderReport.py tests

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
from typing import Literal
import datetime
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageGrab
import base64
import io
from test_paths import TestsOutputPath, TestsReportsPath, TestsSeleniumScreenShootsPath

class HtmlTestStepSliderReport:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
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
        for file in os.listdir(self.selenium_screenshots_path):
            os.remove(os.path.join(self.selenium_screenshots_path, file))

        self.current_test = {
            'name': name
        }

    def end_test(self, name, attrs):
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_name = self.current_test["name"] + " " + today.replace(":", "-")
        path_to_report = os.path.abspath(os.path.join(self.reports_path, test_name))

        if not os.path.exists(path_to_report):
            os.mkdir(path_to_report)

        path_to_report = os.path.join(path_to_report, "report_step_slider")
        os.mkdir(path_to_report)

        env = Environment(loader=FileSystemLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "static", 'templates'))
            )
        )
        template = env.get_template('step_slider_report.html')
        output = template.render(testname=self.current_test["name"], steps_data=self.keywords_config + self.keywords_data)
        with open(os.path.join(path_to_report, self.current_test["name"] + ".html"), "w", encoding="utf-8") as f:
            f.write(output)

        self.keywords_data = []
        self.screenshot_element_counter = 1
        self.screenshot_counter = 1

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
