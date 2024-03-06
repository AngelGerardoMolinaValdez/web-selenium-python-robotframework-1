*** Settings ***
Documentation
...    Este archivo tiene la finalidad de importar las librerías necesarias para la ejecución de los casos de prueba
...    Esto con el fin de no tener que importar las librerías en cada archivo de prueba ya que librerias como
...    SeleniumLibrary, necesitan una previa configuración para su uso. Por ejemplo:
...    - Que hacer al fallar
...    - La carpeta de capturas de pantalla
...    - El tiempo de espera

Library    SeleniumLibrary
...    timeout=20 seconds
...    run_on_failure=${None}
...    screenshot_root_directory=${EXECDIR}/output/selenium-screenshots
