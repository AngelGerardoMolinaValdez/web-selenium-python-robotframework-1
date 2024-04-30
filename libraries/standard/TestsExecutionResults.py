import os
from dataclasses import dataclass, fields, is_dataclass
from util.test_paths import TestsOutputPath, TestsResultsPath
from util.file_results_writers import ResultWriterType

class TestsExecutionResults:
    """TestsExecutionResults es una librería que permite guardar la información de la ejecución de los tests en un archivo de datos.

    Las funcionalidades se integran con la librería DataTableLibrary.py de este proyecto, es decir, se puede utilizar un DataTable para guardar la información de la ejecución de los tests, sin embargo, se puede adaptar también a diccionarios.

    Estos resultados se guardaran por ejecución y no por caso de prueba, es decir, si se ejecutan 3 test cases, se guardaran los resultados de los 3 test cases en un solo archivo de datos.

    Los resultados se guardaran en un archivo CSV por defecto, pero se puede cambiar a JSON si se desea.

    La carpeta asignada para esto es output/results, sin embargo, se puede cambiar si se desea con el argumento output_dir en la keyword `Save Test Execution Results`.

    = Guardar los resultados de la ejecución de los tests =
    Data la siguiente DataTable:
    | ${dt}    VAR    DataTable(name="Foo", age=12, city="New York", country="EUA", email="fake@mail.com", phone="5565656565")

    Se puede guardar la información de la siguiente manera:
    | Save Test Execution Results    ${dt}

    Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
    | name,age,city,country,email,phone
    | Foo,12,New York,EUA,fake@mail.com,5565656565

    o en JSON:
    | Save Test Execution Results    ${dt}    JSON

    y esto genera un archivo JSON con el siguiente contenido:
    | [
    |     {
    |         "name": "Foo",
    |         "age": 12,
    |         "city": "New York",
    |         "country": "EUA",
    |         "email": "fake@mail.com",
    |         "phone": "5565656565"
    |     }
    | ]

    Y una vez creado este archivo la información se agregara a este mismo hasta que se termina la ejecución.

    = Guardar DataTables con diferentes campos =
    Se puede guardar DataTables con diferentes campos en el mismo archivo de datos, por ejemplo:
    | *** Settings ***
    | Library    ./libraries/TestsExecutionResults.py
    |
    | *** Variables ***
    | ${dt1}    DataTable(name="Foo", age=12, city="New York", country="EUA", email="fake@mail.com")
    | ${dt2}    DataTable(name="Bar", age=24, city="Los Angeles", country="EUA", email="fake@mail.com", phone="5565656565")

    Se puede guardar la información de la siguiente manera:
    | *** Test Cases ***
    | Test 1
    |     Save Test Execution Results    ${dt1}
    |
    | Test 2
    |     Save Test Execution Results    ${dt2}

    Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
    | name,age,city,country,email,phone
    | Foo,12,New York,EUA,
    | Bar,24,Los Angeles,EUA,5565656565

    El campo que no tenia el DataTable 1 se agrego como vacío.

    = Trabajar con diccionarios =
    Se puede trabajar con diccionarios en lugar de DataTables, por ejemplo:
    | *** Settings ***
    | Library    ./libraries/TestsExecutionResults.py
    |
    | *** Variables ***
    | ${dt1}    {"name": "Foo", "age": 12, "city": "New York", "country": "EUA", "email": "email@mx.com"}

    Se puede guardar la información de la siguiente manera:
    | *** Test Cases ***
    | Test 1
    |     Save Test Execution Results    ${dt1}

    = Consideraciones =
    - El nombre del archivo de datos será TestExecutionResults[index].csv.
    - Se debe invocar una vez por bloque de test cases, es decir, si se tienen 3 test cases, se debe invocar una vez por bloque de test cases. Si se invoca más de una vez, se sobrescribirá el archivo de datos.
    - Los campos que no estaban en el DataTable anterior se agregaran al final
    - Se recomienda invocar la keyword `Save Test Execution Results` al final de cada bloque de test cases, para evitar que se sobrescriba el archivo de datos.
    - No se pueden guardar en diferentes tipos de archivos en una misma ejecución, es decir, si se guarda en CSV, no se puede guardar en JSON en la misma ejecución.
    """
    __file__name: str = None
    __file_path: str = None
    __results_dir: str = None

    def __new__(cls):
        if cls.__file_path is None:
            output_path = TestsOutputPath().path()
            cls.__results_dir = TestsResultsPath().path()

            file_name = f"TestExecutionResults{cls.__get_file_index(cls.__results_dir)}."
            cls.__file__name = file_name
            cls.__file_path = os.path.join(cls.__results_dir)
        return super().__new__(cls)

    def save_test_execution_results_from_fields(self, type_output="CSV", encoding="utf-8", output_dir=None, **kwargs):
        """Guardar los resultados de la ejecución de los tests en un archivo de datos sin utilizar un DataTable como fuente de información.

        === Descripción de los argumentos ===
        1. type_output: (str) Tipo de archivo de datos a guardar. Puede ser CSV o JSON. Por defecto es CSV.

        2. encoding: (str) Codificación del archivo de datos. Por defecto es utf-8.

        3. outputdir: (str) Directorio donde se guardara el archivo de datos. Por defecto es output/results.

        4. kwargs: (dict) Campos a guardar en el archivo de datos.

        === Ejemplo de uso ===
        | Save Test Execution Results From Fields    name="Foo"    age=12    city="New York"    country="EUA"
        | Save Test Execution Results From Fields    name="Foo"    age=12    city="New York"    country="EUA"    is_active=True   output_dir=output/results

        Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
        | name,age,city,country,is_active
        | Foo,12,New York,EUA,
        | Foo,12,New York,EUA,True

        o en JSON:
        | Save Test Execution Results From Fields    name="Foo"    age=12    city="New York"    country="EUA"    is_active=True    JSON

        y esto genera un archivo JSON con el siguiente contenido:
        | [
        |     {
        |         "name": "Foo",
        |         "age": 12,
        |         "city": "New York",
        |         "country": "EUA",
        |         "is_active": null
        |     },
        |     {
        |         "name": "Foo",
        |         "age": 12,
        |         "city": "New York",
        |         "country": "EUA",
        |         "is_active": true
        |     }
        | ]

        === Consideraciones ===
        - El nombre del archivo de datos será TestExecutionResults[index].csv.
        - Se debe invocar una vez por bloque de test cases, es decir, si se tienen 3 test cases, se debe invocar una vez por bloque de test cases. Si se invoca más de una vez, se sobrescribirá el archivo de datos.
        - Los campos que no estaban en el DataTable anterior se agregaran al final
        - Se recomienda invocar la keyword `Save Test Execution Results` al final de cada bloque de test cases, para evitar que se sobrescriba el archivo de datos.
        - No se pueden guardar en diferentes tipos de archivos en una misma ejecución, es decir, si se guarda en CSV, no se puede guardar en JSON en la misma ejecución.
        - Si se define un encoding que no es soportado, se generara un error.
        """
        test_data = kwargs

        path = output_dir if output_dir else self.__file_path
        file_name = f"TestExecutionResults{self.__get_file_index(output_dir)}." if output_dir else self.__file__name
        # el resultado final en ambos casos es un diccionario
        self.__save_test_results(test_data, path, file_name, type_output, encoding)

    def __serialize_dataclass_to_flat_dict(self, dataclass_instance, parent_key=''):
        """ Serializa una dataclass (incluyendo dataclasses anidadas) a un diccionario plano con claves anidadas como strings."""
        items = {}
        for field_name, field_type in dataclass_instance.__annotations__.items():
            key = f"{parent_key}.{field_name}" if parent_key else field_name
            value = getattr(dataclass_instance, field_name)
            if is_dataclass(value):
                items.update(self.__serialize_dataclass_to_flat_dict(value, key))
            else:
                items[key] = value
        return items

    def save_test_execution_results(self, data_table, type_output="CSV", encoding="utf-8", output_dir=None):
        """Guardar los resultados de la ejecución de los tests en un archivo de datos utilizando un DataTable como fuente de información.

        === Descripción de los argumentos ===
        1. data_table: (DataTable) DataTable con la información de la ejecución de los tests.

        2. type_output: (str) Tipo de archivo de datos a guardar. Puede ser CSV o JSON. Por defecto es CSV.
        
        3. encoding: (str) Codificación del archivo de datos. Por defecto es utf-8.
        
        4. outputdir: (str) Directorio donde se guardara el archivo de datos. Por defecto es output/results.

        === Ejemplo de uso ===
        | VAR   ${DT1}  DataTable(name="Foo", age=12, city="New York", country="EUA")
        | VAR   ${DT2}  DataTable(name="Foo", age=12, city="New York", country="EUA", is_active=True)
        | Save Test Execution Results    ${DT1}
        | Save Test Execution Results    ${DT2}
        | Save Test Execution Results    ${DT1}    JSON
        | Save Test Execution Results    ${DT2}    encoding=utf-16

        Y esto generara un archivo CSV con el nombre del test suite con el siguiente contenido:
        | name,age,city,country,is_active
        | Foo,12,New York,EUA,
        | Foo,12,New York,EUA,True

        o en JSON:
        | Save Test Execution Results    ${DT1}    JSON
        | Save Test Execution Results    ${DT2}    JSON

        y esto genera un archivo JSON con el siguiente contenido:
        | [
        |     {
        |         "name": "Foo",
        |         "age": 12,
        |         "city": "New York",
        |         "country": "EUA",
        |         "is_active": null
        |     },
        |     {
        |         "name": "Foo",
        |         "age": 12,
        |         "city": "New York",
        |         "country": "EUA",
        |         "is_active": true
        |     }
        | ]

        === Consideraciones ===
        - El nombre del archivo de datos será TestExecutionResults[index].csv.
        - Se debe invocar una vez por bloque de test cases, es decir, si se tienen 3 test cases, se debe invocar una vez por bloque de test cases. Si se invoca más de una vez, se sobrescribirá el archivo de datos.
        - Los campos que no estaban en el DataTable anterior se agregaran al final
        - Se recomienda invocar la keyword `Save Test Execution Results` al final de cada bloque de test cases, para evitar que se sobrescriba el archivo de datos.
        - No se pueden guardar en diferentes tipos de archivos en una misma ejecución, es decir, si se guarda en CSV, no se puede guardar en JSON en la misma ejecución.
        - Si se define un encoding que no es soportado, se generara un error.
        """
        test_data = self.__serialize_dataclass_to_flat_dict(data_table)

        path = output_dir if output_dir else self.__file_path
        file_name = f"TestExecutionResults{self.__get_file_index(output_dir)}." if output_dir else self.__file__name
        self.__save_test_results(test_data, path, file_name, type_output, encoding)

    @classmethod
    def __get_file_index(cls, path):
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return len(files)

    def __save_test_results(self, test_data: dataclass, path, file_name, type_output, encoding):
        file_path = os.path.join(path, f"{file_name}{type_output.lower()}")
        reader = ResultWriterType[type_output.upper()].value
        reader.write(file_path, test_data, encoding)
