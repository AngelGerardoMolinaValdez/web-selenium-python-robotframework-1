"""
Esta librería permite resaltar elementos en la página web durante la ejecución de pruebas.

Es util para resaltar elementos en la página web durante la ejecución de pruebas, para que los usuarios puedan ver claramente que elementos están siendo afectados por las pruebas.

#### Iluminación de elementos

La iluminación de elementos se puede realizar de varias maneras, incluyendo:

1. **Resaltado Permanente:** Resalta un elemento de forma permanente con un color específico y un estilo de borde.
2. **Resaltado Asíncrono:** Resalta un elemento con un color específico y un estilo de borde durante un tiempo específico y luego restaura el estilo original.
3. **Resaltado de Gradiente:** Aplica un gradiente de arcoíris continuo en el borde de un elemento.
4. **Resaltado de Gradiente Cónico:** Aplica un gradiente cónico que rota alrededor del borde de un elemento web.
5. **Resaltado de Gradiente Móvil:** Aplica un gradiente de arcoíris continuo que se mueve alrededor del borde de un elemento indefinidamente.
6. **Resaltado de Gradiente Suave:** Resalta un elemento con una transición suave entre múltiples colores en el fondo usando animación de CSS.
7. **Resaltado de Gradiente Suave en Borde:** Resalta un elemento con una transición suave entre múltiples colores usando animación de CSS.

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

#### Estilos de Borde

Puedes personalizar el estilo del borde de los elementos resaltados en tus pruebas automatizadas con Selenium y Robot Framework. Los estilos de borde disponibles incluyen:

1. **Solid:** Un borde sólido.
2. **Dotted:** Un borde punteado.
3. **Dashed:** Un borde discontinuo.
4. **Double:** Un borde doble.
5. **Groove:** Un borde en relieve.
6. **Ridge:** Un borde en relieve.
7. **Inset:** Un borde en relieve.
8. **Outset:** Un borde en relieve.

#### Sombra

Puedes añadir una sombra a los elementos resaltados en tus pruebas automatizadas con Selenium y Robot Framework. La sombra se puede añadir con la propiedad `box-shadow` de CSS. Por ejemplo, para añadir una sombra de 5px de ancho y 5px de desplazamiento en todas las direcciones, puedes hacer lo siguiente:

```python
highlight_element('id:tu-id-elemento', shadow='5px 5px 5px #888888')
```

#### Opacidad de Relleno

Puedes añadir una opacidad de relleno a los elementos resaltados en tus pruebas automatizadas con Selenium y Robot Framework. La opacidad de relleno se puede añadir con la función `rgba()` de CSS. Por ejemplo, para añadir un relleno con un 10% de opacidad, puedes hacer lo siguiente:

```python
highlight_element('id:tu-id-elemento', fill_opacity=0.1)
```

#### Animación

Puedes añadir animación a los elementos resaltados en tus pruebas automatizadas con Selenium y Robot Framework. La animación se puede añadir con la propiedad `transition` de CSS. Por ejemplo, para añadir una animación de 0.5 segundos al resaltar un elemento, puedes hacer lo siguiente:

```python
highlight_element('id:tu-id-elemento', with_animation=True, seconds=0.5)
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

#### Consideraciones

- Al usar selectores web con el caracter `=`, se debe colocar una diagonal invertida `\` antes del caracter `=`, para que no sea interpretado como un operador de asignación. Ejemplo: `id\=your-element-id`. Esto ultimo se puede evitar si el locator se guarda previamente en una variable y se pasa como argumento a la función.
"""
from robot.libraries.BuiltIn import BuiltIn


class HighLightLibrary:
    def __init__(self, border_style="solid", border_width="4px", color="blue", with_animation=True, seconds=0.5, shadow=None, fill_opacity=0.1):
        self.__border_style = border_style
        self.__border_width = border_width
        self.__color = color
        self.__with_animation = with_animation
        self.__seconds = seconds
        self.__shadow = shadow
        self.__fill_opacity = fill_opacity
        self.__colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'cyan', 'magenta', 'lime', 'gray', 'black', 'white']
        self.__borders = ['solid', 'dotted', 'dashed', 'double', 'groove', 'ridge', 'inset', 'outset']
        self.__highlighted_elements = []
        self.__update_style()

    def __update_style(self):
        shadow_style = f"box-shadow: {self.__shadow};" if self.__shadow else ""
        animation_style = f"transition: border-color {self.__seconds}s ease-in-out, background-color {self.__seconds}s ease-in-out;" if self.__with_animation else ""
        background_color = f"background-color: {self.__convert_to_rgba(self.__color, self.__fill_opacity)};"
        border_color = self.__color
        self.__default_style = f"border: {self.__border_width} {self.__border_style} {border_color}; {background_color}{shadow_style}{animation_style}"

    def __convert_to_rgba(self, color, opacity=1.0):
        if "rgba" in color:
            return color
        elif "rgb" in color:
            return color.replace("rgb", "rgba").replace(")", f", {opacity})")
        elif color.startswith('#'):
            return f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, {opacity})"
        else:
            return f"rgba({self.__name_to_rgb(color)}, {opacity})"

    def __name_to_rgb(self, name):
        color_map = {
            'red': '255, 0, 0',
            'green': '0, 128, 0',
            'blue': '0, 0, 255',
            'yellow': '255, 255, 0',
            'orange': '255, 165, 0',
            'purple': '128, 0, 128',
            'pink': '255, 192, 203',
            'cyan': '0, 255, 255',
            'magenta': '255, 0, 255',
            'lime': '0, 255, 0',
            'gray': '128, 128, 128',
            'black': '0, 0, 0',
            'white': '255, 255, 255'
        }
        return color_map.get(name, '0, 0, 0')

    def __get_selenium_instances(self):
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        return (selenium_lib, selenium_lib.driver)

    def set_style_default(self, **kwargs):
        style_updated = False

        for key, value in kwargs.items():
            attr_name = f'_HighLightLibrary__{key}'
            if hasattr(self, attr_name) and getattr(self, attr_name) != value:
                setattr(self, attr_name, value)
                style_updated = True

        if style_updated:
            self.__update_style()

    def highlight_element_persistent(self, locator, **style_kwargs):
        self.set_style_default(**style_kwargs)
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        driver.execute_script("arguments[0].setAttribute('style', `${arguments[1]} ${arguments[2]}`);", element, self.__default_style, original_style)

    def highlight_element_async(self, locator, duration=1000, **style_kwargs):
        self.set_style_default(**style_kwargs)
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        highlight_style = self.__default_style
        
        script = f"""
        var element = arguments[0];
        var newStyle = '{highlight_style}' + ' ' + arguments[1];
        element.setAttribute('style', newStyle);
        setTimeout(function() {{
            element.setAttribute('style', arguments[1]);  // Restaura el estilo original después de la duración especificada
        }}, {duration});
        """
        driver.execute_script(script, element, original_style)

    def highlight_elements_persistent(self, *locators, **style_kwargs):
        for locator in locators:
            self.highlight_element_persistent(locator, **style_kwargs)

    def highlight_elements_async(self, *locators, duration=3000, **style_kwargs):
        for locator in locators:
            self.highlight_element_async(locator, duration, **style_kwargs)
    
    def fade_highlight_elements_persistent(self, *locators, duration=7000):
        for locator in locators:
            self.fade_highlight_element_persistent(locator, duration)

    def rainbow_static_highlight_elements_persistent(self, *locators):
        for locator in locators:
            self.rainbow_static_highlight_element_persistent(locator)

    def rainbow_static_highlight_elements_async(self, *locators, duration=3000):
        for locator in locators:
            self.rainbow_static_highlight_element_async(locator, duration)

    def fade_animated_fill_elements_persistent(self, *locators, duration=7000):
        for locator in locators:
            self.fade_animated_fill_element_persistent(locator, duration)

    def rainbow_animated_fill_elements_persistent(self, *locators):
        for locator in locators:
            self.rainbow_animated_fill_element_persistent(locator)

    def rainbow_animated_highlight_elements_persistent(self, *locators, duration=5000):
        for locator in locators:
            self.rainbow_animated_highlight_element_persistent(locator, duration)

    def remove_highlight(self, locator):
        """Remove any highlight styles from the element."""
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        original_style = element.get_attribute('data-original-style') or ""
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)

    def remove_all_highlights(self):
        """
        Elimina el estilo de resaltado de todos los elementos resaltados almacenados que aún son visibles.
        """
        seleniumlib, driver = self.__get_selenium_instances()
        for locator in self.__highlighted_elements:
            try:
                element = seleniumlib.find_element(locator)
                original_style = element.get_attribute('data-original-style') or ""
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)
            except Exception as e:
                print(f"No se pudo encontrar el elemento con locator {locator}. Error: {e}")
        
        self.__highlighted_elements.clear()

    def fade_highlight_element_persistent(self, locator, duration=7000):
        """
        Resalta un elemento con una transición suave entre múltiples colores usando animación de CSS.

        Args:
            locator (str): El localizador del elemento a resaltar.
            duration (int): Duración total de la animación en milisegundos.

        Example:
            fade_highlight_element_smooth('id:your-element-id', 7000)
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = f"""
        var element = arguments[0];
        var originalStyle = arguments[1];
        var duration = arguments[2];

        var keyframes = `
            @keyframes colorFade {{
                0%   {{ border-color: red; }}
                25%  {{ border-color: yellow; }}
                50%  {{ border-color: blue; }}
                75%  {{ border-color: cyan; }}
                100% {{ border-color: green; }}
            }}
        `;

        var styleSheet = document.createElement('style');
        styleSheet.type = 'text/css';
        styleSheet.innerText = keyframes;
        document.head.appendChild(styleSheet);

        var animationStyle = 'animation: colorFade ' + (duration / 1000) + 's infinite;';
        element.setAttribute('style', 'border: 4px solid; ' + animationStyle + originalStyle);
        """
        driver.execute_script(script, element, original_style, duration)

    def rainbow_static_highlight_element_persistent(self, locator):
        """
        Aplica un gradiente de arcoíris continuo en el borde de un elemento de forma permanente.

        Args:
            locator (str): El localizador del elemento a resaltar.

        Example:
            rainbow_static_highlight_element_persistent('id:your-element-id')
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = """
        var element = arguments[0];
        var gradientStyle = `
            background: linear-gradient(
                to right, 
                red, 
                orange, 
                yellow, 
                green, 
                blue, 
                indigo, 
                violet
            );
            -webkit-background-clip: text;
            color: transparent;
            border: 4px solid;
            border-image-source: linear-gradient(
                to right, 
                red, 
                orange, 
                yellow, 
                green, 
                blue, 
                indigo, 
                violet
            );
            border-image-slice: 1;
        `;
        
        element.setAttribute('style', gradientStyle + arguments[1]);
        """
        driver.execute_script(script, element, original_style)

    def rainbow_static_highlight_element_async(self, locator, duration=3000):
        """
        Aplica un gradiente de arcoíris continuo en el borde de un elemento.

        Args:
            locator (str): El localizador del elemento a resaltar.
            duration (int): Duración de la animación del gradiente en milisegundos.

        Example:
            highlight_element_rainbow_gradient('id:your-element-id', duration=5000)
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = """
        var element = arguments[0];
        var originalStyle = arguments[1];
        var duration = arguments[2];
        var gradientStyle = `
            background: linear-gradient(
                to right, 
                red, 
                orange, 
                yellow, 
                green, 
                blue, 
                indigo, 
                violet
            );
            -webkit-background-clip: text;
            color: transparent;
            border: 4px solid;
            border-image-source: linear-gradient(
                to right, 
                red, 
                orange, 
                yellow, 
                green, 
                blue, 
                indigo, 
                violet
            );
            border-image-slice: 1;
        `;
        
        element.setAttribute('style', gradientStyle + originalStyle);

        // Eliminar el estilo después de un tiempo especificado
        setTimeout(function() {
            element.setAttribute('style', originalStyle);
        }, duration);
        """
        driver.execute_script(script, element, original_style, duration)

    def fade_animated_fill_element_persistent(self, locator, duration=7000):
        """
        Resalta un elemento con una transición suave entre múltiples colores en el fondo usando animación de CSS.

        Args:
            locator (str): El localizador del elemento a resaltar.
            duration (int): Duración total de la animación en milisegundos.

        Example:
            fade_highlight_element_persistent('id:your-element-id', 7000)
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = f"""
        var element = arguments[0];
        var originalStyle = arguments[1];
        var duration = arguments[2];

        var keyframes = `
            @keyframes colorFade {{
                0%   {{ background-color: red; }}
                25%  {{ background-color: yellow; }}
                50%  {{ background-color: blue; }}
                75%  {{ background-color: cyan; }}
                100% {{ background-color: green; }}
            }}
        `;

        var styleSheet = document.createElement('style');
        styleSheet.type = 'text/css';
        styleSheet.innerText = keyframes;
        document.head.appendChild(styleSheet);

        var animationStyle = 'animation: colorFade ' + (duration / 1000) + 's infinite;';
        element.setAttribute('style', 'border: 4px solid transparent; ' + animationStyle + originalStyle);
        """
        driver.execute_script(script, element, original_style, duration)

    def rainbow_animated_fill_element_persistent(self, locator):
        """
        Aplica un gradiente de arcoíris continuo que se mueve alrededor del borde de un elemento indefinidamente.

        Args:
            locator (str): El localizador del elemento a resaltar.

        Example:
            continuous_moving_rainbow_highlight_element('id:your-element-id')
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = """
        var element = arguments[0];
        var originalStyle = arguments[1];
        var gradientStyle = `
            border: 4px solid transparent;
            background: linear-gradient(
                124deg, 
                #ff2400, #e81d1d, #e8b71d, #e3e81d, #1de840, #1ddde8, #2b1de8, #dd00f3, #dd00f3
            );
            background-size: 1800% 1800%;
            animation: moveGradient 18s ease infinite;
        `;

        var keyframes = `
            @keyframes moveGradient {
                0% { background-position: 0% 82%; }
                50% { background-position: 100% 19%; }
                100% { background-position: 0% 82%; }
            }
        `;

        // Agregar los keyframes al documento
        var styleSheet = document.createElement('style');
        styleSheet.type = 'text/css';
        styleSheet.innerText = keyframes;
        document.head.appendChild(styleSheet);

        element.setAttribute('style', gradientStyle + originalStyle);
        """
        driver.execute_script(script, element, original_style)

    def rainbow_animated_highlight_element_persistent(self, locator, duration=5000):
        """
        Aplica un gradiente cónico que rota alrededor del borde de un elemento web.

        Args:
            locator (str): El localizador del elemento a resaltar.
            duration (int): Duración de la animación en milisegundos.

        Example:
            conic_gradient_border_highlight('name:username', duration=10000)
        """
        seleniumlib, driver = self.__get_selenium_instances()
        element = seleniumlib.find_element(locator)
        self.__highlighted_elements.append(locator)
        original_style = element.get_attribute('style')
        script = """
        var element = arguments[0];
        var originalStyle = arguments[1];
        var duration = arguments[2];
        var gradientStyle = `
            border: 4px solid;
            border-image: conic-gradient(from var(--angle), red, yellow, lime, aqua, blue, magenta, red) 1;
        `;

        var keyframes = `
            @keyframes rotate {
                to {
                    --angle: 360deg;
                }
            }
        `;

        var property = `
            @property --angle {
                syntax: '<angle>';
                initial-value: 0deg;
                inherits: false;
            }
        `;

        var animationStyle = `
            animation: ${duration/1000}s rotate linear infinite;
        `;

        // Agregar los keyframes y la propiedad CSS al documento
        var styleSheet = document.createElement('style');
        styleSheet.type = 'text/css';
        styleSheet.innerText = keyframes + property;
        document.head.appendChild(styleSheet);

        element.setAttribute('style', gradientStyle + animationStyle + originalStyle);
        """
        driver.execute_script(script, element, original_style, duration)
