import os
from dataclasses import dataclass, make_dataclass, asdict
from file_readers import FileReaderType


class DataTableLibrary:
    """
    DataTableLibrary es una librería de Robot Framework que permite crear DataTables a partir de un archivo CSV o JSON y acceder a los datos de la fila como atributos del objeto.

    Esta librería esta hecho con el fin de reducir la declaración de variables en el archivo de pruebas, ya que se puede crear un DataTable a partir de un archivo CSV y acceder a los datos de la fila como atributos del objeto. Se crean dataclasses dinamicas en base a un archivo csv.

    Un DataTable es una estructura de datos que representa una tabla de datos. Este se crea a partir de una lista de diccionarios, donde cada diccionario representa una fila de la tabla y este mismo diccionario se convierte en un dataclass para poder acceder a los datos de la fila como atributos del objeto.

    Un `dataclass` es una funcionalidad de Python 3.7 que simplifica la creación de clases para almacenar datos. Mediante el módulo `dataclasses`, automatiza la generación de métodos como `__init__()`, `__repr__()`, `__eq__()`, y `__hash__()`, esenciales en clases usadas principalmente como contenedores de datos.

    = Crear un DataTable =
    Con los siguientes datos de prueba:

    *data.csv*
    | name,age,city,country
    | John Doe,30,New York,USA
    | Jane Doe,25,San Francisco,USA

    | *** Test Cases ***
    | Create DataTable
    |     ${table}=    Create Data Table    ${CURDIR}/data.csv    0
    |     Log    ${table}
    |     Log    ${table.name}
    |     Log    ${table.age}
    |     Log    ${table.city}
    |     Log    ${table.country}

    Dando como resultado:

    | DataTable(name='John Doe', age='30', city='New York', country='USA')

    También es posible con un archivo JSON:

    *data.json*
    | [
    |     {
    |         "name": "John Doe",
    |         "age": 30,
    |         "city": "New York",
    |         "country": "USA"
    |     },
    |     {
    |         "name": "Jane Doe",
    |         "age": 25,
    |         "city": "San Francisco",
    |         "country": "USA"
    |     }
    | ]

    Esta estructura de datos crea el mismo DataTable que el archivo CSV.

    = Crear DataTable sin archivo de datos =

    Los data tables se crean a partir de un archivo CSV o JSON, pero también se pueden crear a partir de un diccionario de datos.

    | *** Test Cases ***
    | Create DataTable From Fields
    |     ${table}=    Create Data Table From Fields    name=John Doe    age=30    city=New York    country=USA
    |     Log    ${table}
    |     Log    ${table.name}
    |     Log    ${table.age}
    |     Log    ${table.city}
    |     Log    ${table.country}
    |     Log    ${table.email}
    |     Log    ${table.phone}

    Dando como resultado:
    | DataTable(name='John Doe', age='30', city='New York', country='USA')

    = Agregar un campo al DataTable =
    Con los siguientes datos de prueba:

    *data.csv*
    | name,age,city,country
    | John Doe,30,New York,USA
    | Jane Doe,25,San Francisco,USA

    o tambien con un json:

    *data.json*
    | [
    |     {
    |         "name": "John Doe",
    |         "age": 30,
    |         "city": "New York",
    |         "country": "USA"
    |     },
    |     {
    |         "name": "Jane Doe",
    |         "age": 25,
    |         "city": "San Francisco",
    |         "country": "USA"
    |     }
    | ]

    Se puede agregar un campo al DataTable de la siguiente manera:

    | *** Test Cases ***
    | Add Field
    |     ${table}=    Create Data Table    ${CURDIR}/data.csv    0
    |     ${new_table}=    Update Data Table    ${table}   is_active=True
    |     Log    ${new_table.is_alive}

    Dando como resultado:
    | DataTable(name='John Doe', age='30', city='New York', country='USA', is_active='True')

    También es posible agregar varios campos al DataTable:

    | *** Test Cases ***
    | Add Field
    |     ${table}=    Create Data Table    ${CURDIR}/data.csv    0
    |     ${new_table}=    Update Data Table    ${table}   is_active=True     account_type=premium

    Dando como resultado:
    | DataTable(name='John Doe', age='30', city='New York', country='USA', is_active='True', account_type='premium')

    = Unir dos DataTables =

    Con los siguientes datos de prueba:

    *data.csv*
    | name,age,city,country
    | John Doe,30,New York,USA
    | Jane Doe,25,San Francisco,USA

    *data2.csv*
    | email,phone
    | foo@mail.com,123456789
    | bar@mail.com,123456789

    Se pueden unir dos DataTables de la siguiente manera:

    | *** Test Cases ***
    | Merge DataTables
    |     ${table1}=    Create Data Table    ${CURDIR}/data.csv    0
    |     ${table2}=    Create Data Table    ${CURDIR}/data2.csv    0
    |     ${new_table}=    Merge Data Tables    ${table1}    ${table2}
    |     Log    ${new_table}

    Dando como resultado:
    | DataTable(name='John Doe', age='30', city='New York', country='USA', email='foo@mail.com', phone='123456789')

    = Unir varios DataTables =

    Con los siguientes datos de prueba:

    *data.csv*
    | name,age,city,country
    | John Doe,30,New York,USA
    | Jane Doe,25,San Francisco,USA

    *data2.csv*
    | email,phone
    | foo@mail.com,123456789
    | bar@mail.com,123456789

    *data3.csv*
    | is_active
    | True
    | False

    Se pueden unir varios DataTables de la siguiente manera:

    | *** Test Cases ***
    | Unify DataTables
    |     ${table1}=    Create Data Table    ${CURDIR}/data.csv    0
    |     ${table2}=    Create Data Table    ${CURDIR}/data2.csv    0
    |     ${table3}=    Create Data Table    ${CURDIR}/data3.csv    0
    |     ${new_table}=    Unify Data Tables    ${table1}    ${table2}    ${table3}
    |     Log    ${new_table}

    Dando como resultado:
    | DataTable(name='John Doe', age='30', city='New York', country='USA', email='foo@mail.com', phone='123456789', is_active='True')

    = Consideraciones =

    - El índice de la fila inicia en 0.
    - Los nombres de las columnas del archivo de datos deben ser únicos.
    - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
    - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
    """

    def create_data_table(self, path: str, index: int) -> dataclass:
        """Crea un DataTable a partir de un archivo CSV o JSON.

        === Descripción de los argumentos ===
        - `path`: Ruta del archivo CSV o JSON.
        - `index`: Índice de la fila del archivo de datos.

        === Ejemplo de uso ===
        | ${table}=    Create Data Table    ${CURDIR}/data.csv    0
        | Log    ${table}
        | Log    ${table.name}
        | Log    ${table.age}

        | ${table}=    Create Data Table    ${CURDIR}/data.json    0
        | Log    ${table}
        | Log    ${table.name}
        | Log    ${table.age}

        === Consideraciones ===
        - El índice de la fila inicia en 0.
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        """
        ext_file = os.path.splitext(path)[1]
        reader = FileReaderType[ext_file[1:].upper()].value
        reader.read(path)
        test_data_row = reader.get(index)
        DataTable: dataclass = make_dataclass("DataTable", test_data_row.keys())
        return DataTable(**test_data_row)

    def create_data_table_from_fields(self, **fields) -> dataclass:
        """Crea un DataTable a partir de un diccionario de datos.

        === Descripción de los argumentos ===
        - `fields`: Campos del DataTable.

        === Ejemplo de uso ===
        | ${table}=    Create Data Table From Fields    name=John Doe    age=30    city=New York    country=USA
        | Log    ${table}
        | Log    ${table.name}
        | Log    ${table.age}

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        """
        DataTable: dataclass = make_dataclass("DataTable", fields.keys())
        return DataTable(**fields)

    def update_data_table(self, data_table: dataclass, **fields) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable.

        === Descripción de los argumentos ===
        - `data_table`: DataTable.
        - `fields`: Campos del DataTable.

        === Ejemplo de uso ===
        | ${table}=    Create Data Table From Fields    name=John Doe    age=30    city=New York    country=USA     is_alive=False
        | ${new_table}=    Update Data Table    ${table}   is_active=True
        | Log    ${new_table.is_alive}

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        """
        data_class_dict = asdict(data_table)
        data_class_dict.update(fields)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in data_class_dict.keys()]
        )
        return DataClass(**data_class_dict)

    def merge_data_tables(self, data_table: dataclass, another_data_table: dataclass) -> dataclass:
        """Actualiza un DataTable con los campos de otro DataTable y retorna una nueva instancia del DataTable.

        === Descripción de los argumentos ===
        - `data_table`: DataTable.
        - `another_data_table`: DataTable.

        === Ejemplo de uso ===
        | ${table1}=    Create Data Table From Fields    name=John Doe    age=30
        | ${table2}=    Create Data Table From Fields    city=New York    country=USA     is_alive=False
        | ${new_table}=    Merge Data Tables    ${table1}    ${table2}
        | Log    ${new_table}
        | Log    ${new_table.is_alive}
        | Log    ${new_table.name}

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        - El primer DataTable se actualiza con los campos del segundo DataTable.
        """
        data_table_dict = asdict(data_table)
        another_data_table_dict = asdict(another_data_table)
        data_table_dict.update(another_data_table_dict)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in data_table_dict.keys()]
        )
        return DataClass(**data_table_dict)

    def unify_data_tables(self, data_table: dataclass, *data_tables) -> dataclass:
        """Unifica varios DataTables y retorna una nueva instancia del DataTable.

        === Descripción de los argumentos ===
        - `data_table`: DataTable.
        - `data_tables`: DataTables.

        === Ejemplo de uso ===
        | ${table1}=    Create Data Table From Fields    name=John Doe    age=30
        | ${table2}=    Create Data Table From Fields       city=New York    country=USA     is_alive=False
        | ${table3}=    Create Data Table From Fields       premium=True    account_type=premium
        | ${new_table}=    Unify Data Tables    ${table1}    ${table2}    ${table3}
        | Log    ${new_table}
        | Log    ${new_table.is_alive}
        | Log    ${new_table.name}
        | Log    ${new_table.account_type}

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        - Se unifican varios DataTables en un solo DataTable.
        - El primer DataTable se actualiza con los campos de los siguientes DataTables.
        """
        original_data_table_dict = asdict(data_table)
        for another_data_table in data_tables:
            another_data_table_dict = asdict(another_data_table)
            original_data_table_dict.update(another_data_table_dict)
        DataClass = make_dataclass(
            "DataClass",
            [(name, str) for name in original_data_table_dict.keys()]
        )
        return DataClass(**original_data_table_dict)
