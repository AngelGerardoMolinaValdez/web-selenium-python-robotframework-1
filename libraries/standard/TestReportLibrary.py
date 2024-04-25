from robot.libraries.BuiltIn import BuiltIn
from test_report_library_context.test_report_details import TestReportDetails
from test_report_library_context.test_report_context import TestReportContext
from test_report_library_context.reports.report_creator import ReportCreator

class TestReportLibrary:
    """Test Report Library es una librearía que permite generar reportes de pruebas de manera dinámica.
    Los reportes pueden ser generados en formato PDF, HTML Vertical Slider y HTML Horizontal Slider.

    Robot Framework ya ofrece reportes de ejecución de test cases, pero no ofrece un reporte de los pasos de ejecución de un test case.

    Esta libreria tiene dos formas de crear un reporte:
    - Con la keyword `Create Report` se puede generar un reporte con los pasos de ejecución de un test case.
    - Con el listener TestReportGenerator se puede generar un reporte al finalizar la ejecución de un test case.

    Estas formas solo van enfocadas en la creacion del archivo y no en la toma de evidencia para los reportes.

    = Formatos =
    == PDF ==
    En este formato se genera un reporte en formato PDF con los pasos de ejecución de un test case.

    Para agregar este formato se debe agregar el argumento *PDF_SLIDER* en la instancia de la librería TestReportLibrary o listener.

    == HTML Vertical Slider ==
    Este reporte muestra los pasos de la ejecución de la prueba con imágenes en un formato vertical.

    En el reporte estan las siguientes funcionalidades:

    - Alternar entre dark mode y light mode.
    - Navegar con el scroll del mouse o desde la ruta de navegación de lado derecho. En esta ruta de navegación se puede navegar por el numero de la captura o por una barra de desplazamiento.
    - Contraer/Expandir los pasos de la prueba (Uno por uno o desde el boton "contraer/expandir todo").
    - Expandir la imagen de la captura de pantalla.
    - Ir a la ultima/primera captura de pantalla.

    Para agregar este formato se debe agregar el argumento *HTML_VERTICAL_SLIDER* en la instancia de la librería TestReportLibrary o listener.

    == HTML Horizontal Slider ==
    Este reporte muestra los pasos de la ejecución de la prueba con imágenes en un formato horizontal.

    En el reporte estan las siguientes funcionalidades:

    - Alternar entre dark mode y light mode.
    - Navegar con los botones "Siguiente" y "Anterior"
    - Expandir la imagen de la captura de pantalla.
    - Ir a la ultima/primera captura de pantalla.

    Para agregar este formato se debe agregar el argumento *HTML_HORIZONTAL_SLIDER* en la instancia de la librería TestReportLibrary o listener.

    = Ejemplos =
    == Crear reporte con la keyword Create Report ==
    | Create Report     ${TEST_NAME}    ${PREV_TEST_STATUS}   PDF_SLIDER  HTML_VERTICAL_SLIDER    HTML_HORIZONTAL_SLIDER
    | Create Report     ${TEST_NAME}    ${PREV_TEST_STATUS}   PDF_SLIDER
    
    == Crear reporte con el listener TestReportGenerator ==
    | robot --listener TestsReportGenerator:PDF_SLIDER:HTML_VERTICAL_SLIDER:HTML_HORIZONTAL_SLIDER tests/
    | robot --listener TestsReportGenerator:PDF_SLIDER tests/

    == Estatus ==
    - *INFO:* Información general. Se utiliza para describir un paso. Contexto de ejemplo: "Se abre la página de inicio".
    - *PASS:* Éxito. Se utiliza para describir un paso que se ejecuto correctamente. Contexto de ejemplo: "Se ingreso el usuario correctamente".
    - *CRITICAL:* Error crítico. Se utiliza para describir un paso que fallo y no se puede continuar con la ejecución. Contexto de ejemplo: "No se pudo ingresar el usuario".
    - *FAIL:* Error. Se utiliza para describir un paso que fallo pero se puede continuar con la ejecución. Contexto de ejemplo: "No se pudo ingresar el usuario".
    - *FALTA:* Falta de implementación. Se utiliza para describir un paso que no se ha implementado. Contexto de ejemplo: "Falta implementar el ingreso de usuario".
    - *WARNING:* Advertencia. Se utiliza para describir un paso que se ejecuto correctamente pero con advertencias. Contexto de ejemplo: "Se ingreso el usuario correctamente pero se tardo mucho".
    - *DEBUG:* Depuración. Se utiliza para describir un paso que se ejecuto correctamente pero se necesita información adicional. Contexto de ejemplo: "Se ingreso el usuario correctamente. Se tardo 5 segundos".
    
    El valor predeterminado es *INFO*.

    = Consideraciones =
    - El reporte se genera con el nombre del caso de prueba
    - El reporte se genera en la carpeta ./base/output/reports/
    - El reporte se genera con la fecha y hora de la ejecución
    - Se pueden especificar desde 1 hasta todos los formatos de reporte disponibles
    - Si se utiliza el listener TestReportGenerator y la keyword `Create Report` en el mismo test case la keyword sera ignorada
    - Al crear el reporte con la keyword `Create Report` se debe especificar el nombre del caso de prueba y el estado del test case
    - Al usar el listener TestReportGenerator no es necesario especificar el estado y nombre del test case, ya que se toma el estado del test case de Robot Framework
    - Si se define el estado del test case con la keyword `Set Test Status` este estado será el que se tome en cuenta para el reporte tanto para la keyword como para el listener
    """
    def __get_selenium_driver(self):
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        return selenium_lib.driver

    def __get_selenium_instance(self):
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        return selenium_lib

    def add_step(self, title, status, is_keyword_setup=False, is_keyword_teardown=False):
        """Agrega un paso al reporte de la prueba.
        
        === Descripción de los argumentos ===
        - `title`: Título del paso.
        - `status`: Estado del paso.
        - `is_keyword_setup`: Indica si el paso es un setup.
        - `is_keyword_teardown`: Indica si el paso es un teardown.

        === Ejemplo de uso ===
        | Add Step     Se abre la página de inicio    INFO

        === Consideraciones ===
        - El estado del paso puede ser INFO, PASS, CRITICAL, FAIL, FALTA, WARNING o DEBUG.
        - El valor predeterminado es INFO.
        - Si el paso es un setup se debe especificar `is_keyword_setup=True`. Esto para que se agregue en todos los reportes. Ejemplo, un login que solo se haga una vez pero sea necesario para todos los tests.
        - Si el paso es un teardown se debe especificar `is_keyword_teardown=True`. Esto para que se agregue en todos los reportes. Ejemplo, un logout que solo se haga una vez pero sea necesario para todos los tests.
        """
        TestReportDetails.add(title, status, setup=is_keyword_setup, teardown=is_keyword_teardown)

    def add_step_capture(self, title, status, is_keyword_setup=False, is_keyword_teardown=False):
        """Agrega un paso al reporte de la prueba con una captura de pantalla.
        
        === Descripción de los argumentos ===
        - `title`: Título del paso.
        - `status`: Estado del paso.
        - `is_keyword_setup`: Indica si el paso es un setup.
        - `is_keyword_teardown`: Indica si el paso es un teardown.

        === Ejemplo de uso ===
        | Add Step Capture     Se abre la página de inicio    INFO

        === Consideraciones ===
        - El estado del paso puede ser INFO, PASS, CRITICAL, FAIL, FALTA, WARNING o DEBUG.
        - El valor predeterminado es INFO.
        - Si el paso es un setup se debe especificar `is_keyword_setup=True`. Esto para que se agregue en todos los reportes. Ejemplo, un login que solo se haga una vez pero sea necesario para todos los tests.
        - Si el paso es un teardown se debe especificar `is_keyword_teardown=True`. Esto para que se agregue en todos los reportes. Ejemplo, un logout que solo se haga una vez pero sea necesario para todos los tests.
        """
        driver = self.__get_selenium_driver()
        capture_base64 = driver.get_screenshot_as_base64()
        TestReportDetails.add(title, status, capture_base64, setup=is_keyword_setup, teardown=is_keyword_teardown)

    def add_step_capture_element(self, title, locator, status, is_keyword_setup=False, is_keyword_teardown=False):
        """Agrega un paso al reporte de la prueba con una captura de pantalla de un elemento.
        
        === Descripción de los argumentos ===
        - `title`: Título del paso.
        - `locator`: Localizador del elemento.
        - `status`: Estado del paso.
        - `is_keyword_setup`: Indica si el paso es un setup.
        - `is_keyword_teardown`: Indica si el paso es un teardown.

        === Ejemplo de uso ===
        | Add Step Capture Element     Se abre la página de inicio    id=elementId    INFO

        === Consideraciones ===
        - El estado del paso puede ser INFO, PASS, CRITICAL, FAIL, FALTA, WARNING o DEBUG.
        - El valor predeterminado es INFO.
        - Si el paso es un setup se debe especificar `is_keyword_setup=True`. Esto para que se agregue en todos los reportes. Ejemplo, un login que solo se haga una vez pero sea necesario para todos los tests.
        - Si el paso es un teardown se debe especificar `is_keyword_teardown=True`. Esto para que se agregue en todos los reportes. Ejemplo, un logout que solo se haga una vez pero sea necesario para todos los tests.
        """
        driver = self.__get_selenium_instance()
        element = driver.find_element(locator)
        element_base64 = element.screenshot_as_base64
        TestReportDetails.add(title, status, element_base64, setup=is_keyword_setup, teardown=is_keyword_teardown)

    def set_test_status(self, status):
        """Establece el estado del caso de prueba.

        Esto es util para definir un estado diferente al que se obtiene de la ejecución del test case.
        
        === Descripción de los argumentos ===
        - `status`: Estado del caso de prueba.

        === Ejemplo de uso ===
        | Set Test Status    PASS

        === Consideraciones ===
        - El estado del caso de prueba puede ser INFO, PASS, CRITICAL, FAIL, FALTA, WARNING o DEBUG.
        - El valor predeterminado es INFO.
        """
        TestReportContext.set_status_defined_in_keyword()
        TestReportDetails.set_status(status)

    def clear_all_steps(self):
        """Limpia todos los pasos de la prueba.
        
        Esto es util cuando se ejecutan multiples suites y se ha guardado informacion de setup y teardown de otros tests que no se desea mostrar.
        
        === Ejemplo de uso ===
        | Clear All Steps
        
        === Consideraciones ===
        - Se eliminan todos los pasos de la prueba.
        - Se eliminan todos los pasos de setup.
        - Se eliminan todos los pasos de teardown.
        """
        TestReportDetails.clear_all()

    def create_report(self, test_name, status, *formats):
        """Crea un reporte de la prueba.
        
        === Descripción de los argumentos ===
        - `test_name`: Nombre del caso de prueba.
        - `status`: Estado del caso de prueba.
        - `formats`: Formatos del reporte.

        === Ejemplo de uso ===
        | Create Report     ${TEST_NAME}    ${PREV_TEST_STATUS}   PDF_SLIDER  HTML_VERTICAL_SLIDER    HTML_HORIZONTAL_SLIDER
        | Create Report     ${TEST_NAME}    ${PREV_TEST_STATUS}   PDF_SLIDER

        === Consideraciones ===
        - El estado del caso de prueba puede ser INFO, PASS, CRITICAL, FAIL, FALTA, WARNING o DEBUG.
        - El valor predeterminado es INFO.
        - Se pueden especificar desde 1 hasta todos los formatos de reporte disponibles.
        - El reporte se genera con el nombre del caso de prueba.
        - El reporte se genera en la carpeta ./base/output/reports/.
        - El reporte se genera con la fecha y hora de la ejecución.
        - Si se ha especificado el listener TestReportGenerator en el mismo test case la keyword sera ignorada.
        """
        if not TestReportContext.get_executed_from_listener():
            ReportCreator().create_report(test_name, status, *formats)
