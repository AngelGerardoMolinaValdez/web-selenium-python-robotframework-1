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

- [Python](https://www.python.org/downloads/) (>=3.9)
- Tu navegador favorito como: [GoogleChrome](https://www.google.com/intl/es-419/chrome/), [FireFox](https://www.mozilla.org/es-MX/firefox/new/), etc
- Algún controlador web de tu navegador favorito como: [ChromeDriver](https://chromedriver.chromium.org/downloads), [GeckoDriverFirefox](https://github.com/mozilla/geckodriver/releases)

NOTA: El controlador web debe ser del navegador que vas a utilizar, ejemplo: chrome == chromedriver

## 🔗 Instalación

Los módulos que usamos en este proyecto los gestionamos con [Poetry](https://python-poetry.org/), para instalarlo ejecutaremos el comando:

- `pip install poetry==1.7.1`

Hecho esto, podremos instalar las dependencias para ejecución:

- `poetry install`
<<<<<<< HEAD
=======

## 📦 Gestión de dependencias

Si necesitas agregar más dependencias, puedes hacerlo con el comando:

- `poetry add <nombre-de-la-dependencia>`

Si necesitas eliminar dependencias, puedes hacerlo con el comando:

- `poetry remove <nombre-de-la-dependencia>`
>>>>>>> dev

## ⚙ Configuración

Es necesario hacer algunas cosas mas para que puedas ejecutar:

- Guarda en una carpeta el ejecutable del controlador web que hayas elegido
- Agregar a las variables de entorno **PATH** (Sistema o usuario) la ruta de la carpeta donde esta dicho controlador.

NOTA: Algunas veces es necesario reiniciar la consola de comandos que vayas a utilizar.

## 📁 Estructura de Carpetas

Este proyecto de scripts automatizados se implementaron varios patrones de arquitectura de pruebas:

- **Page Object Model (POM):** Este patrón se utiliza para mejorar el mantenimiento de las pruebas y reducir la duplicación de código. Los objetos de cada página de la aplicación se representan como archivos .resource en la carpeta pages. Estos objetos se adaptan a las palabras clave para su uso en los casos de prueba.

- **Data Driven Testing (DDT):** Este patrón permite que los casos de prueba se ejecuten con diferentes conjuntos de datos. Los archivos de datos para DDT se almacenan en la carpeta data. Según el número total de filas en el archivo CSV, se ejecutará la suite de pruebas correspondiente.

- **Keyword Driven:** Este patrón implica la definición de palabras clave personalizadas que representan acciones de nivel superior que se pueden utilizar en los casos de prueba. Las palabras clave se almacenan en la carpeta keywords y se invocan desde los casos de prueba.

- **Workflow Pattern:** Este patrón se utiliza para definir una secuencia de pasos (o "flujo de trabajo") que se deben seguir en un caso de prueba. En este proyecto, los flujos de trabajo se definen en la carpeta tests, que contiene los casos de prueba que se ejecutarán.

```bash
project/
--libraries/ # librerías externas
--data/ # los archivos de datos para DDT
--pages/ # los archivos .resource que representaran los objetos de cada pagina de la aplicacion (adaptada a keywords)
--keywords/ # las palabras clave que se usaran para invocarse desde los casos de prueba
--tests/ # los casos de prueba que se ejecutaran
```

## 🚀 Ejecución de Pruebas

Para ejecutar las pruebas, abrir la terminal y ejecutar el comando:

- `poetry run robot ...[options] [file]`

Por ejemplo:

- `poetry run robot --outputdir results/ tests/e2e.robot`

## 📊 Análisis de código

Un linter es una herramienta utilizada para analizar automáticamente el código fuente en busca de errores.

En este proyecto se utilizo el linter de [RoboCop](https://github.com/MarketSquare/robotframework-robocop).

Para obtener el análisis del código, hay que estar en la carpeta raíz del proyecto y ejecutar el comando:

- `poetry run robocop`

Este comando generara en la terminal un resumen de todos los issues encontrados
