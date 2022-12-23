# Casos de prueba automatizados con Robot Framework

Flujos automatizados del sitio web publico [Parabank](https://parabank.parasoft.com/parabank/index.htm).


Este sitio web es publico, por ende las credenciales se guardan en los mismos archivos sin suponer un riesgo.


Casos de prueba diseñados con la version de [Robot Framework](https://robotframework.org/) - [6.0.1](https://github.com/robotframework/robotframework/milestone/66?closed=1).

Version de [Python](https://github.com/robotframework/robotframework/milestone/66?closed=1) - [3.9.0](https://www.python.org/downloads/release/python-390/).

Navegador [Chrome](https://www.google.com/intl/es_mx/chrome/) Version 108.

[Chrome Driver](https://chromedriver.chromium.org/downloads) para Chrome 108


# Requerimientos
## Aplicaciones
- Python
- Chrome
- Webdriver

## Python Extensiones
- robotframework
- robotframework-seleniumlibrary
- PyYAML


# Comandos de ejecucion

## Ejecucion por suite
```robot *.robot```

```robot main.robot```


## Ejecucion por caso de prueba
```robot --test "Abrir Nueva Cuenta Tipo SAVINGS" main.robot```

```robot --test "Abrir Nueva Cuenta Tipo CHECKING" main.robot```

```robot --test "Obtener Resumen De Cuentas" main.robot```



