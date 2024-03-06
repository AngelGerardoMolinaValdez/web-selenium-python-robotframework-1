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
import datetime
from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageGrab
import base64
import io

class HtmlTestStepSliderReport:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.keyword_config = False
        self.keywords_config = []
        self.keywords_data = []
        self.current_test = {}
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        if not os.path.exists(os.path.join(self.base_path, "output")):
            os.mkdir(os.path.join(self.base_path, "output"))

        if not os.path.exists(os.path.join(self.base_path, "output", "reports")):
            os.mkdir(os.path.join(self.base_path, "output", "reports"))

        self.execution_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "reports"))

    def start_test(self, name, attrs):
        self.current_test = {
            'name': name
        }

    def end_test(self, name, attrs):
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path_to_report = os.path.abspath(os.path.join(self.execution_path, self.current_test["name"] + " " + today.replace(":", "-")))

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

    def start_keyword(self, name, attrs):
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        tag_message_title = re.search(r"STEP:IMAGE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FATAL|WARNING|DEBUG))?(?:===|:|$)", "===>".join(attrs['tags']))

        if tag_message_title:
            image_content = self.__take_screenshot()
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
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
        tag_message_title = re.search(r"STEP:IMAGE:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FALTA|WARNING|DEBUG))?(?:===|:|$)", message['message'])

        if tag_message_title:
            image_content = self.__take_screenshot()
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title
            step_data["step_image"] = image_content

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)

    def __take_screenshot(self):
        image_path = os.path.join(self.execution_path,"imagen.png")

        im1 = ImageGrab.grab()
        im1.save(image_path)

        im = Image.open(image_path)
        buff = io.BytesIO()
        im.save(buff, format="PNG")
        os.remove(image_path)

        return base64.b64encode(buff.getvalue()).decode("utf-8")