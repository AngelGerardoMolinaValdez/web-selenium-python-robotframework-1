"""Librería que permite guardar la información de la ejecución de los tests en un archivo de datos.

Las funcionalidades se integran con la librería DataTableLibrary.py de este proyecto, es decir, se puede utilizar un DataTable para guardar la información de la ejecución de los tests, sin embargo, se puede adaptar a cualquier estructura de datos.

Estos resultados se guardaran por ejecución y no por caso de prueba, es decir, si se ejecutan 3 test cases, se guardaran los resultados de los 3 test cases en un solo archivo de datos.

La carpeta asignada para esto es output/results.

## Importar la librería
*** Settings ***
Library    ./libraries/TestsExecutionResults.py

## Guardar los resultados de la ejecución de los tests
Data la siguiente DataTable:
`${dt}    VAR    DataTable(name="Foo", age=12, city="New York", country="EUA", email="fake@mail.com", phone="5565656565")`

Se puede guardar la información de la siguiente manera:
```
Save Test Execution Results    ${dt}
```

Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
```
name,age,city,country,email,phone
Foo,12,New York,EUA,5565656565
```

Y una vez creado este archivo la información se agregara a este mismo hasta que se termina la ejecución.

## Guardar DataTables con diferentes campos
Se puede guardar DataTables con diferentes campos en el mismo archivo de datos, por ejemplo:
```robot
*** Settings ***
Library    ./libraries/TestsExecutionResults.py

*** Variables ***
${dt1}    DataTable(name="Foo", age=12, city="New York", country="EUA", email="fake@mail.com")
${dt2}    DataTable(name="Bar", age=24, city="Los Angeles", country="EUA", email="fake@mail.com", phone="5565656565")
```

Se puede guardar la información de la siguiente manera:
```
*** Test Cases ***
Test 1
    Save Test Execution Results    ${dt1}

Test 2
    Save Test Execution Results    ${dt2}
```

Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
```
name,age,city,country,email,phone
Foo,12,New York,EUA,
Bar,24,Los Angeles,EUA,5565656565
```

El campo que no tenia el DataTable 1 se agrego como vacío.

## Trabajar con diccionarios
Se puede trabajar con diccionarios en lugar de DataTables, por ejemplo:
```robot
*** Settings ***
Library    ./libraries/TestsExecutionResults.py

*** Variables ***
${dt1}    {"name": "Foo", "age": 12, "city": "New York", "country": "EUA", "email": "

Se puede guardar la información de la siguiente manera:
```
*** Test Cases ***
Test 1
    Save Test Execution Results    ${dt1}
```

## Consideraciones
- El nombre del archivo de datos será TestExecutionResults[index].csv.
- Se debe invocar una vez por bloque de test cases, es decir, si se tienen 3 test cases, se debe invocar una vez por bloque de test cases. Si se invoca más de una vez, se sobrescribirá el archivo de datos.
- Los campos que no estaban en el DataTable anterior se agregaran al final
- Se recomienda invocar la keyword `Save Test Execution Results` al final de cada bloque de test cases, para evitar que se sobrescriba el archivo de datos.
"""
import csv
import os
from dataclasses import dataclass, fields


class TestsExecutionResults:
    __file_path: str = None
    __results_dir: str = None

    def __new__(cls):
        if cls.__file_path is None:
            cd = os.path.dirname(__file__)
            cls.__results_dir = os.path.abspath(os.path.join(cd, "..", "output","results"))

            if not os.path.exists(cls.__results_dir):
                os.makedirs(cls.__results_dir)

            file_name = f"TestExecutionResults{cls.__get_file_index()}.csv"
            cls.__file_path = os.path.join(cls.__results_dir, file_name)
        return super().__new__(cls)

    def save_test_execution_results(self, data_table):
        """Guarda la información de la ejecución de los tests en un archivo de datos.

        Args:
        - data_table: DataTable con la información a guardar.
        """
        try:
            test_data = dict(data_table)
        except:
            all_fields = {}
            for field in fields(data_table):
                all_fields[field.name] = getattr(data_table, field.name)
            test_data = all_fields

        self._save_data_table_to_csv(test_data, self.__file_path)
    
    @classmethod
    def __get_file_index(cls):
        files = [f for f in os.listdir(cls.__results_dir) if os.path.isfile(os.path.join(cls.__results_dir, f))]
        return len(files)

    def _save_data_table_to_csv(self, test_data: dataclass, file_name):
        file_path = os.path.join(self.__results_dir, file_name)
        # Intentar leer los campos existentes del archivo CSV
        try:
            with open(file_path, mode='r', newline='') as f:
                lector = csv.reader(f)
                campos_existentes = next(lector, [])
        except FileNotFoundError:
            campos_existentes = []

        # Determinar si hay nuevos campos en el nuevo registro
        campos_nuevos = set(test_data.keys()) - set(campos_existentes)
        campos_actualizados = campos_existentes + list(campos_nuevos)

        if campos_nuevos:
            # Crear un archivo temporal para escribir los datos actualizados
            archivo_temporal = file_path + '.tmp'
            
            with open(archivo_temporal, mode='w', newline='') as f_temp:
                escritor = csv.DictWriter(f_temp, fieldnames=campos_actualizados)
                escritor.writeheader()

                # Si el archivo original existe, copiar los datos existentes al temporal
                if campos_existentes:
                    with open(file_path, mode='r', newline='') as f_orig:
                        lector = csv.DictReader(f_orig)
                        for fila in lector:
                            escritor.writerow(fila)
                
                # Agregar el nuevo registro al archivo temporal
                escritor.writerow(test_data)

            # Reemplazar el archivo original con el temporal
            os.replace(archivo_temporal, file_path)
        else:
            # Simplemente agregar el nuevo registro si no hay campos nuevos
            with open(file_path, mode='a', newline='') as f:
                escritor = csv.DictWriter(f, fieldnames=campos_existentes)
                if not campos_existentes:  # Si es el primer registro, escribir la cabecera
                    escritor.writeheader()
                escritor.writerow(test_data)