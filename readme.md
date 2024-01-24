# 🤖 Proyecto de Automatización con Robot Framework 🚀

## 📖 Introducción

Robot Framework es un marco de trabajo (framework) de código abierto para la automatización de pruebas y la automatización de procesos de aceptación (ATDD, Acceptance Test-Driven Development). Es utilizado para automatizar pruebas funcionales, pruebas de aceptación, pruebas de sistemas, etc.

Puntos clave sobre Robot Framework:

1. **Sintaxis Simple y Legible**: Robot Framework utiliza una sintaxis simple basada en palabras clave (keywords) que facilita la escritura y lectura de pruebas, incluso para personas sin un fondo técnico fuerte.

2. **Extensible**: Puede ser extendido con bibliotecas (libraries) externas, que pueden ser implementadas en Python o Java. Esto permite a los usuarios añadir funcionalidades específicas o interactuar con sistemas y aplicaciones de una manera personalizada.

3. **Integración con Herramientas Existentes**: Robot Framework puede integrarse con otras herramientas populares de pruebas y CI/CD como Selenium, Appium, Jenkins, entre otras.

4. **Rico en Funcionalidades**: Ofrece una amplia variedad de funcionalidades out-of-the-box, incluyendo la gestión de variables, la configuración de la suite de pruebas, la ejecución condicional, entre otros.

5. **Reportes y Logs**: Genera informes y logs detallados y de fácil lectura que ayudan en la identificación y solución de problemas.

6. **Multiplataforma**: Funciona en la mayoría de los sistemas operativos y puede automatizar aplicaciones web, móviles y de escritorio.

Visita el [sitio oficial de Robot Framework](https://robotframework.org) para mas información.

## ☑️ Requisitos

Para que este proyecto funcione necesitamos:

- [Python](https://www.python.org/downloads/) (>=3.11)
- [Robot Framework](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary)
- Tu navegador favorito como: [GoogleChrome](https://www.google.com/intl/es-419/chrome/), [FireFox](https://www.mozilla.org/es-MX/firefox/new/), etc
- Algún controlador web de tu navegador favorito como: [ChromeDriver](https://chromedriver.chromium.org/downloads), [GeckoDriverFirefox](https://github.com/mozilla/geckodriver/releases)

NOTA: El controlador web debe ser del navegador que vas a utilizar, ejemplo: chrome == chromedriver

## 🔗 Instalación

Los módulos que usamos en este proyecto los gestionamos con [Poetry](https://python-poetry.org/), para instalarlo ejecutaremos el comando:

- `pip install poetry==1.7.1`

Hecho esto, podremos instalar las dependencias para ejecución:

- `poetry install`

## ⚙ Configuración

Es necesario hacer algunas cosas mas para que puedas ejecutar:

- Guarda en una carpeta el ejecutable del controlador web que hayas elegido
- Agregar a las variables de entorno **PATH** (Sistema o usuario) la ruta de la carpeta donde esta dicho controlador.

NOTA: Algunas veces es necesario reiniciar la consola de comandos que vayas a utilizar.

## 📚 Documentación

La documentación de la librería `TestDataLibrary.py` se encuentra en la carpeta `./data/documentation/`.

## 📁 Estructura de Carpetas

- **data/**: Carpeta donde se guardan los datos utilizados durante la ejecución.
  - **steps/**: Contiene los archivos `.csv` con los datos para la ejecución.
    - **test_data.csv**: el archivo con los datos de prueba
  - **variables/**: Contiene variables globales de la ejecución, como el login, rutas de carpetas, etc.

- **libraries/**: Carpeta para las bibliotecas externas propias generadas.
  - **Datatablelibrary.py**: Biblioteca externa que permite crear data tables para la ejecución.

- **output/**: Carpeta destinada a los archivos generados por ejecución.
  - **results/**: Donde se guardan los archivos de resultados de las pruebas.
  - **reports/**: Carpeta donde se guardan los archivos que genera Robot Framework log, report, output.

- **resources/**: Carpeta para los archivos `.resource` que se implementan para los casos de prueba.

- **scripts/**: Carpeta que contiene los archivos de configuración/ejecución, etc.
  - **run/**: Contiene los archivos de ejecución como `windows.cmd`, `windows.ps1`, `linux.sh`.

- **tests/**: Carpeta que contiene los archivos `.robot`.
  - **steps/**: Contiene los pasos de cada caso de prueba.

## 🚀 Ejecución de Pruebas

Para ejecutar las pruebas, abrir la consola de comandos y ejecutar el script correspondiente al sistema operativo. Cabe mencionar que según el total de filas que haya en el csv serán las veces que se ejecute la suite `tests/steps`

Ejemplo:

- `scripts/run/windows.cmd`

- `scripts/run/linux.sh`

Al ejecutar con estos archivos, se creara la variable `${ITERATION}` que contendrá
el valor numérico de la ejecución. Ejemplo, si el archivo de datos tiene 3 filas, el valor iniciara en 0 e incrementara en 1.

## 📊 Resultados

Los resultados de las pruebas se guardarán en la carpeta `output/results/`. Se crear un archivos TestResults\[index\].csv por cada vez que se ejecute el archivo de `scripts/run/`. Además, los reportes generados por Robot Framework (log.html, report.html, output.xml) se guardaran en `output/reports` con la siguiente estructura: report--\[iteration\]--\[date\]

## 📊 Análisis de código

Un linter es una herramienta utilizada para analizar automáticamente el código fuente en busca de errores.

En este proyecto se utilizo el linter de [RoboCop](https://github.com/MarketSquare/robotframework-robocop).

Para obtener el análisis del código, hay que estar en la carpeta raíz del proyecto y ejecutar el comando:

- `.\scripts\linter\robocop.cmd`

Este comando generara un archivo en `output/linter/` con el nombre `robocop.log`.