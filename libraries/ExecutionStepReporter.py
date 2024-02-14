"""
Es una librería de Robot Framework que permite generar un reporte de los pasos de ejecución de un test case en un archivo de log.
El reporte se genera en un archivo de log con el mismo nombre del test case.
El reporte se genera en la carpeta ./base/output/reports/

Para utilizar la librería, se debe especificar como listener al ejecutar las pruebas:
- robot --listener ExecutionStepReporter.py tests

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
    - Se puede agregar un nivel de log (INFO, FAIL, FATAL, CRITICAL, DEBUG, WARNING) después de agregar el mensaje con el formato STEP:DESCRIPCIÓN DEL PASO:NIVEL, el nivel es opcional y su valor predeterminado es INFO
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
import re
import os

class ExecutionStepReporter:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self._log_file = None
        self._log_file_name = None
        self._log_file_path = None
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self._log_file_content = []

        if not os.path.exists(os.path.join(self.base_path, "output")):
            os.mkdir(os.path.join(self.base_path, "output"))

        if not os.path.exists(os.path.join(self.base_path, "output", "reports")):
            os.mkdir(os.path.join(self.base_path, "output", "reports"))

    def start_test(self, name, attrs):
        self._log_file_name = name + '.log'
        self._log_file_path = os.path.join(self.base_path, "output", "reports", self._log_file_name)
        self._log_file = open(self._log_file_path, 'a', encoding='utf-8')

    def end_test(self, name, attrs):
        self._log_file_content.append("\n[TEST MESSAGE]" + " " + attrs["message"])
        self._log_file.write('\n'.join(self._log_file_content))
        self._log_file.write('\n')
        self._log_file.close()
        self._log_file_content = []
    
    def start_keyword(self, name, attrs):
        if not 'REPORT:LOG' in attrs['tags']:
            return
        self._log_file_content.append("[" + attrs["type"] + "]" + " " + name)

    def end_keyword(self, name, attrs):
        tag_message = re.search(r"STEP:(.+?)(?::(INFO|FAIL|FALTAL|CRITICAL|DEBUG|WARNING))?(?:===|:|$)", "===>".join(attrs['tags']))
        if tag_message:
            level = tag_message.group(2) if tag_message.group(2) else "INFO"
            self._log_file_content.append(f"\t[{level}] " + tag_message.group(1))

        if 'REPORT:LOG' in attrs['tags']:
            self._log_file_content.append("[" + attrs["type"] + "]" + " " + "[" + attrs["status"] + "]" + " " + name)

    def log_message(self, message):
        log_message = re.search(r"STEP:(.+?)(?::(INFO|FAIL|FALTAL|CRITICAL|DEBUG|WARNING))?(?:===|:|$)",message['message'])
        if log_message:
            level = log_message.group(2) if log_message.group(2) else "INFO"
            self._log_file_content.append(f"\t[{level}] " + log_message.group(1))
