"""Librería para la creación de DataTables a partir de archivos CSV.

Esta librería esta hecho con el fin de reducir la declaración de variables en el archivo de pruebas, ya que se puede crear un DataTable a partir de un archivo CSV y acceder a los datos de la fila como atributos del objeto.

Un DataTable es una estructura de datos que representa una tabla de datos. Este se crea a partir de una lista de diccionarios, donde cada diccionario representa una fila de la tabla y este mismo diccionario se convierte en un dataclass para poder acceder a los datos de la fila como atributos del objeto.

Un `dataclass` es una funcionalidad de Python 3.7 que simplifica la creación de clases para almacenar datos. Mediante el módulo `dataclasses`, automatiza la generación de métodos como `__init__()`, `__repr__()`, `__eq__()`, y `__hash__()`, esenciales en clases usadas principalmente como contenedores de datos.

### Importar la librería

```robotframework
*** Settings ***
Library    ./libraries/DataTableLibrary.py
```

### Crear un DataTable
Con los siguientes datos de prueba:

```csv
name,age,city,country
John Doe,30,New York,USA
Jane Doe,25,San Francisco,USA
```

```robotframework
*** Test Cases ***
Create DataTable
    ${table}=    Create Data Table    ${CURDIR}/data.csv    0
    Log    ${table}
    Log    ${table.name}
    Log    ${table.age}
    Log    ${table.city}
    Log    ${table.country}
    Log    ${table.email}
    Log    ${table.phone}
```

### Agregar un campo al DataTable

Con los siguientes datos de prueba:

```csv
name,age,city,country
John Doe,30,New York,USA
Jane Doe,25,San Francisco,USA
```

Se puede agregar un campo al DataTable de la siguiente manera:

```robotframework
*** Test Cases ***
Add Field
    ${table}=    Create Data Table    ${CURDIR}/data.csv    0
    ${new_table}=    Update Data Table    ${table}   is_active   True
    Log    ${new_table}
```

Dando como resultado:

`DataTable(name='John Doe', age='30', city='New York', country='USA', is_active='True')`

### Consideraciones

- El índice de la fila inicia en 0.
- Los nombres de las columnas del archivo de datos deben ser únicos.
- Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
- Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
"""
import os
import csv
from typing import Any
from dataclasses import dataclass, make_dataclass, asdict

class CsvReader:
    __content: list[dict[str, Any]] = []

    @classmethod
    def read(cls, path: str) -> list:
        """Read the CSV file and return a list of dictionaries."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo de datos no existe: {path}")

        with open(path, 'r') as file:
            cls.__content = list(csv.DictReader(file))
    
    @classmethod
    def get(cls, index: int) -> dict:
        try:
            index = int(index)
        except ValueError:
            raise ValueError(f"El índice {index} no es un número entero.")

        if index < 0 or index >= len(cls.__content):
            raise IndexError(f"El índice {index} está fuera de rango de las filas del archivo de datos.")

        return cls.__content[index]


class DataTableLibrary:    
    def create_data_table(self, path: str, index: int) -> dataclass:
        """Crea un DataTable a partir de un archivo CSV."""
        CsvReader.read(path)
        test_data_row = CsvReader.get(index)
        DataTable: dataclass = make_dataclass("DataTable", test_data_row.keys())
        return DataTable(**test_data_row)

    def update_data_table(self, data_table: dataclass, **fields) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable."""
        data_class_dict = asdict(data_table)
        data_class_dict.update(fields)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in data_class_dict.keys()]
        )
        return DataClass(**data_class_dict)
