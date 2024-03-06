"""
### HighLightLibrary.py

Esta librería permite resaltar elementos en la página web durante la ejecución de pruebas.

Es util para resaltar elementos en la página web durante la ejecución de pruebas, para que los usuarios puedan ver claramente que elementos están siendo afectados por las pruebas.

Hay 3 tipos de iluminación:
- `highlight_element_persistent`: Resalta el elemento de forma permanente.
- `highlight_element_sync`: Resalta el elemento de forma sincrona durante un tiempo determinado.
- `highlight_element_async`: Resalta el elemento de forma asíncrona durante un tiempo determinado.

#### Localización de elementos
La localización de elementos se realiza con el uso de Selectors de CSS, Selectors de XPath, Selectors de ID, Selectors de Name, Selectors de Class, Selectors de Tag, Selectors de Link Text, Selectors de Partial Link Text. En pocas palabras, se puede utilizar cualquier selector que se pueda utilizar con SeleniumLibrary.

#### Colores

Para personalizar aún más los colores al iluminar elementos en tus pruebas automatizadas con Selenium y Robot Framework, puedes usar cualquier valor de color que sea válido en CSS. Esto incluye varios tipos de especificaciones de color:

1. **Nombres de Color CSS:** CSS soporta nombres de color predefinidos, como `red`, `green`, `blue`, `yellow`, `orange`, `purple`, `pink`, `cyan`, `magenta`, `lime`, `gray`, `black`, `white`, y muchos más.

2. **Valores Hexadecimales:** Puedes especificar colores usando valores hexadecimales, que comienzan con `#` seguido de 3 o 6 dígitos que representan los componentes de color RGB (Rojo, Verde, Azul). Por ejemplo, `#FF0000` es rojo, `#00FF00` es verde, y `#0000FF` es azul. Los valores hexadecimales pueden ofrecer más de 16 millones de colores.

3. **RGB y RGBA:** La función `rgb()` permite especificar colores en términos de la intensidad de los componentes rojo, verde y azul, con valores que van de 0 a 255. Por ejemplo, `rgb(255, 0, 0)` es rojo. `RGBA` añade un cuarto valor para la opacidad, donde 0 es completamente transparente y 1 es completamente opaco. Por ejemplo, `rgba(255, 0, 0, 0.5)` sería rojo con una opacidad del 50%.

4. **HSL y HSLA:** La función `hsl()` especifica colores en términos de tono (hue), saturación (saturation) y luminosidad (lightness). Por ejemplo, `hsl(0, 100%, 50%)` es rojo. Al igual que con RGBA, `HSLA` añade un componente de opacidad. Por ejemplo, `hsla(0, 100%, 50%, 0.5)` sería rojo con una opacidad del 50%.

Estos tipos de valores te permiten definir prácticamente cualquier color que puedas necesitar para resaltar elementos en tus pruebas. Por ejemplo, si quisieras usar un tono específico de azul que tiene un código hex, o un valor RGB específico para una precisión de color exacta, podrías hacerlo pasando el valor correspondiente al argumento `color` en la función `highlight_element`.

Aquí algunos ejemplos de cómo pasar diferentes tipos de valores de color a tu función `highlight_element`:

- **Usando un nombre de color CSS:**
  ```python
  highlight_element('id:tu-id-elemento', 'cyan')
  ```
  
- **Usando un valor hexadecimal:**
  ```python
  highlight_element('id:tu-id-elemento', '#33cc33')
  ```
  
- **Usando RGB:**
  ```python
  highlight_element('id:tu-id-elemento', 'rgb(255, 165, 0)')  # Orange
  ```
  
- **Usando RGBA (con opacidad):**
  ```python
  highlight_element('id:tu-id-elemento', 'rgba(255, 99, 71, 0.5)')  # Tomato con opacidad del 50%
  ```

#### Uso
```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    HighLightLibrary.py

*** Test Cases ***
Example
    Open Browser    https://www.google.com    chrome
    Highlight Element Persistent    name=q
    Input Text    name=q    robot framework
    Click Element    name=btnK
    Highlight Element Sync    name=q
    Close Browser
```
"""
import time
from robot.libraries.BuiltIn import BuiltIn


class HighLightLibrary:
    def highlight_element_persistent(self, locator, color="blue"):
        self.__seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
        driver = self.__seleniumlib.driver
        element = self.__seleniumlib.find_element(locator)
        original_style = element.get_attribute('style')
        highlight_style = f"border: 4px solid {color};"
        driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, highlight_style + original_style)

    def highlight_element_sync(self, locator, color="blue", duration=1):
        self.__seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
        driver = self.__seleniumlib.driver
        element = self.__seleniumlib.find_element(locator)
        original_style = element.get_attribute('style')
        highlight_style = f"border: 4px solid {color};"
        driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, highlight_style + original_style)
        time.sleep(duration)
        driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, original_style)

    def highlight_element_async(self, locator, color="blue", duration=1000):
        self.__seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
        driver = self.__seleniumlib.driver
        element = self.__seleniumlib.find_element(locator)
        original_style = element.get_attribute('style')
        highlight_style = f"border: 4px solid {color};"
        script = f"""
        arguments[0].setAttribute('style', '{highlight_style}' + arguments[1]);
        setTimeout(function() {{
            arguments[0].setAttribute('style', arguments[1]);
        }}, {duration});
        """
        driver.execute_script(script, element, original_style)
