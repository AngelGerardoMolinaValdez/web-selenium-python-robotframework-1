"""
Es una librería de Robot Framework que permite generar un reporte de los pasos de ejecución de un test case en un archivo de log.
El reporte se genera en un archivo de log con el mismo nombre del test case.
El reporte se genera en la carpeta ./base/output/reports/

Para utilizar la librería, se debe especificar como listener al ejecutar las pruebas:
- robot --listener HtmlTestReportListener1.py tests

Hay dos tipos de acciones que se pueden hacer en el reporte:
1 - Especificar un bloque de pasos que se deben reportar
    - Se debe agregar el tag REPORT:LOG en la keyword
    - Ejemplo:
        *** Keywords ***
        My Keyword
            [Tags]  REPORT:LOG
            Log  Step 1
            Log  Step 2
            Log  Step 3
    Este ejemplo agregara al reporte lo siguiente:
    [KEYWORD] My Keyword
    [KEYWORD] [STATUS] My Keyword 

2 - Especificar un mensaje en un paso
    - Se debe agregar el tag STEP: en el mensaje
    - Se puede agregar un nivel de log (INFO, FAIL, WARN) después de agregar el mensaje con el formato STEP:DESCRIPCIÓN DEL PASO:NIVEL, el nivel es opcional y su valor predeterminado es INFO
    - Ejemplo:
        *** Keywords ***
        My Sub Keyword
            [Tags]  STEP:DESCRIPCIÓN DEL PASO:INFO
            No Operation

        My Other Sub Keyword
            [Tags]  STEP:DESCRIPCIÓN DEL PASO 2
            No Operation

        My Other Sub Keyword
            [Tags]  STEP:DESCRIPCIÓN DEL PASO 3:FAIL
            No Operation

    Este ejemplo agregara al reporte lo siguiente:
    [KEYWORD] My Keyword
        [INFO] DESCRIPCIÓN DEL PASO
        [INFO] DESCRIPCIÓN DEL PASO 2
        [FAIL] DESCRIPCIÓN DEL PASO 3
    [KEYWORD] [STATUS] My Keyword 
    
Cuando usar cada tipo de acción:
- REPORT:LOG: Se debe usar cuando se quiere reportar un bloque de pasos. El bloque de pasos permite ver de manera más clara los pasos que se ejecutan en una keyword.
- STEP: Se debe usar cuando se quiere reportar un mensaje en un paso. El mensaje se puede usar para reportar información adicional de un paso, como por ejemplo, el valor de una variable, el resultado de una operación, etc.

Consideraciones:
- Se puede agregar un STEP: en la misma keyword donde indicamos REPORT:LOG, pero el mensaje se agregara al final del bloque de pasos.
"""
import os
import re
import datetime
from jinja2 import Environment, FileSystemLoader

class HtmlTestReportListener1:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.keyword_data = []
        self.keyword_config = []
        self.accumulator = []
        self.current_test = None
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        if not os.path.exists(os.path.join(self.base_path, "output")):
            os.mkdir(os.path.join(self.base_path, "output"))

        if not os.path.exists(os.path.join(self.base_path, "output", "reports")):
            os.mkdir(os.path.join(self.base_path, "output", "reports"))

        if not os.path.exists(os.path.join(self.base_path, "output", "robot")):
            os.mkdir(os.path.join(self.base_path, "output", "robot"))

    def start_test(self, name, attrs):
        self.current_test = {
            'name': name,
            'doc': attrs['doc'],
            'status': None,
            'message': None,
            'template': attrs['template']
        }

    def end_test(self, name, attrs):
        self.current_test['status'] = attrs['status']
        self.current_test['message'] = attrs['message']

        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path_to_report = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "reports", self.current_test["name"] + " " + today.replace(":", "-")))

        os.mkdir(path_to_report)

        env = Environment(loader=FileSystemLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "static", 'templates'))
            )
        )
        template = env.get_template('step_report_1.html')

        output = template.render(data=[self.keyword_config, self.accumulator], testdata=self.current_test)
        with open(os.path.join(path_to_report, self.current_test["name"] + ".html"), 'w') as f:
            f.write(output)
        
        self.keyword_data = []
        self.accumulator = []

    def start_keyword(self, name, attrs):
        if not 'REPORT:LOG' in attrs['tags']:
            return

        self.keyword_data = {
                'name': name,
                'doc': attrs['doc'],
                'type': attrs['type'],
                'status': None,
                'steps': []
        }

        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config.append(self.keyword_data)
        else:
            self.accumulator.append(self.keyword_data)

    def end_keyword(self, name, attrs):
        tag_message = re.search(r"STEP:(.+?)(?::(INFO|FAIL|WARN))?(?:===|:|$)", "===>".join(attrs['tags']))

        if tag_message:
            level = tag_message.group(2) if tag_message.group(2) else "INFO"
            step_message = tag_message.group(1)
            self.keyword_data['steps'].append({'level': level.lower(), 'message': step_message})

        if 'REPORT:LOG' in attrs['tags']:
            self.keyword_data['status'] = attrs['status']

    def log_message(self, message):
        log_message = re.search(r"STEP:(.+?)(?::(INFO|FAIL|WARN))?(?:===|:|$)",message['message'])
        if log_message:
            level = log_message.group(2) if log_message.group(2) else "INFO"
            self.keyword_data['steps'].append({'level': level, 'message': log_message.group(1)})
