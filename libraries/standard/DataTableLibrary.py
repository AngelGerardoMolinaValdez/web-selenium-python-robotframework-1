import os
from dataclasses import dataclass, make_dataclass, asdict, fields, is_dataclass
from util.file_readers import FileReaderType
from data_table_context.data_table_iterator import DataTableCollection


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

    = Crear un DataTable anidado =

    Con los siguientes datos de prueba:

    *data.csv*
    | user.name,user.age,user.address.city,user.address.country,user.work.company.name,user.work.company.address.city,user.work.company.address.country
    | John Doe,30,New York,USA,Google,Mountain View,USA

    Se puede crear un DataTable anidado de la siguiente manera:

    | *** Test Cases ***
    | Create Nested DataTable
    |     ${table}=    Create Nested Data Table    ${CURDIR}/data.csv    0
    |     Log    ${table} # DataTable(user=DataTable(name='John Doe', age='30', address=DataTable(city='New York', country='USA'), work=DataTable(company=DataTable(name='Google', address=DataTable(city='Mountain View', country='USA')))))
    |     Log    ${table.user.name} # John Doe
    |     Log    ${table.user.age} # 30
    |     Log    ${table.user.address.city} # New York
    |     Log    ${table.user.address.country} # USA
    |     Log    ${table.user.work.company.name} # Google
    |     Log    ${table.user.work.company.address.city} # Mountain View
    |     Log    ${table.user.work.company.address.country} # USA

    Esto ayudara a poder definir estructuras de datos mas complejas y anidadas, ademas que se puede definir el mismo nombre de un campo pero con diferentes contextos dentro de la estructura de datos.

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
    - Se puede utilizar `len()` para obtener la cantidad de campos del DataTable. Por ejemplo `DataTable("name", "age", "city")` retornará 3 al utilizar `len(DataTable)` porque tiene 3 campos.
    """
    def __create_data_class(self, fields_values) -> dataclass:
        DataTable: dataclass = make_dataclass("DataTable", fields_values.keys())

        def dataclass_len(self):
            return len(fields(self))
        DataTable.__len__ = dataclass_len

        return DataTable(**fields_values)

    def create_data_table(self, path: str, index: int, encoding="utf-8") -> dataclass:
        """Crea un DataTable a partir de un archivo CSV o JSON.

        === Descripción de los argumentos ===
        - `path`: Ruta del archivo CSV o JSON.
        - `index`: Índice de la fila del archivo de datos.
        - `encoding`: Codificación del archivo de datos. Por defecto es utf-8.

        === Ejemplo de uso ===
        | ${table}=    Create Data Table    ${CURDIR}/data.csv    0
        | Log    ${table}
        | Log    ${table.name}
        | Log    ${table.age}

        | ${table}=    Create Data Table    ${CURDIR}/data.json    0    encoding=utf-16
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
        reader.read(path, encoding)
        test_data_row = reader.get(index)
        return self.__create_data_class(test_data_row)

    def __parse_nested_fields(self, fields):
        nested_dict = {}
        for field in fields:
            parts = field.split('.')
            current = nested_dict
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = str
        return nested_dict

    def __create_dataclass_from_nested_dict(self, name, nested_dict):
        fields = []
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                nested_class = self.__create_dataclass_from_nested_dict(key, value)
                fields.append((key, nested_class))
            else:
                fields.append((key, value))
        return make_dataclass(name, fields)

    def __create_nested_dataclass(self, name, fields):
        nested_dict = self.__parse_nested_fields(fields)
        return self.__create_dataclass_from_nested_dict(name, nested_dict)

    def __parse_keys_to_nested_dict(self, data_values):
        """Parse flattened dict keys into a nested dictionary."""
        result = {}
        for key, value in data_values.items():
            parts = key.split('.')
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    def __fill_dataclass_values(self, dataclass, data_values):
        data_dict = {}
        for field_name, field_type in dataclass.__annotations__.items():
            if is_dataclass(field_type):
                sub_data_values = data_values.get(field_name, {})
                data_dict[field_name] = self.__fill_dataclass_values(field_type, sub_data_values)
            else:
                data_dict[field_name] = data_values.get(field_name)
        return dataclass(**data_dict)

    def create_nested_data_table(self, path: str, index: int, encoding="utf-8"):
        """Crea un DataTable a partir de un archivo CSV o JSON y retorna un DataTable anidado.

        === Descripción de los argumentos ===

        - `path`: Ruta del archivo CSV o JSON.
        - `index`: Índice de la fila del archivo de datos.
        - `encoding`: Codificación del archivo de datos. Por defecto es utf-8.

        === Ejemplo de uso ===
        
        Dado el siguiente archivo CSV:

        *data.csv*
        | user.name,user.age,user.address.city,user.address.country,user.work.company.name,user.work.company.address.city,user.work.company.address.country
        | John Doe,30,New York,USA,Google,Mountain View,USA

        Se puede crear un DataTable anidado de la siguiente manera:

        | ${table}=    Create Nested Data Table    ${CURDIR}/data.csv    0
        | Log    ${table} # DataTable(user=DataTable(name='John Doe', age='30', address=DataTable(city='New York', country='USA'), work=DataTable(company=DataTable(name='Google', address=DataTable(city='Mountain View', country='USA')))))
        | Log    ${table.user.name} # John Doe
        | Log    ${table.user.age} # 30
        | Log    ${table.user.address.city} # New York
        | Log    ${table.user.address.country} # USA
        | Log    ${table.user.work.company.name} # Google
        | Log    ${table.user.work.company.address.city} # Mountain View
        | Log    ${table.user.work.company.address.country} # USA

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        - Si se aplicara anidación a un DataTable que no tiene un campo anidado, se creará un DataTable con un campo anidado vacío.
        - Para anidar correctamente los campos, se debe seguir la convención de nombres de los campos. Por ejemplo, si se desea anidar el campo `address.city`, se debe separar los campos con un punto `.`.
        """
        ext_file = os.path.splitext(path)[1].lower().strip('.')
        reader = FileReaderType[ext_file.upper()].value
        reader.read(path, encoding)
        data_values = reader.get(index)

        nested_data_values = self.__parse_keys_to_nested_dict(data_values)

        headers = list(data_values.keys())
        dataclass = self.__create_nested_dataclass('DataTable', headers)
        return self.__fill_dataclass_values(dataclass, nested_data_values)

    def create_data_table_from_fields(self, **field_values) -> dataclass:
        """Crea un DataTable a partir de un diccionario de datos.

        === Descripción de los argumentos ===
        - `field_values`: Campos del DataTable.

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
        return self.__create_data_class(field_values)

    def create_data_table_iterator(self, path: str, encoding="utf-8") -> dataclass:
        """Crea un iterador de DataTables a partir de un archivo CSV o JSON.

        === Descripción de los argumentos ===
        - `path`: Ruta del archivo CSV o JSON.
        - `encoding`: Codificación del archivo de datos. Por defecto es utf-8.

        === Ejemplo de uso ===
        | ${iterator}=    Create Data Table Iterator    ${CURDIR}/data.csv
        | FOR    ${table}    IN    @{iterator}
        |    Log    ${table}
        |    Log    ${table.name}
        |    Log    ${table.age}

        | ${iterator}=    Create Data Table Iterator    ${CURDIR}/data.json
        | FOR    ${table}    IN    @{iterator}
        |    Log    ${table}
        |    Log    ${table.name}
        |    Log    ${table.age}

        === Consideraciones ===
        - Los nombres de las columnas del archivo de datos deben ser únicos.
        - Los nombres de las columnas del archivo de datos no deben contener espacios en blanco.
        - Los nombres de las columnas del archivo de datos no deben contener tildes ni caracteres especiales.
        """
        ext_file = os.path.splitext(path)[1]

        reader = FileReaderType[ext_file[1:].upper()].value
        reader.read(path, encoding)
        test_data_row = reader.get_all()

        collection = DataTableCollection()
        for row in test_data_row:
            collection.add_data_table(self.__create_data_class(row))
        iterator = collection.create_iterator()

        return iterator

    def update_data_table(self, data_table: dataclass, **field_values) -> dataclass:
        """Agrega un nuevo campo al DataTable y retorna una nueva instancia del DataTable.

        === Descripción de los argumentos ===
        - `data_table`: DataTable.
        - `field_values`: Campos del DataTable.

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
        data_class_dict.update(field_values)
        return self.__create_data_class(data_class_dict)

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

        return self.__create_data_class(data_table_dict)

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
        return self.__create_data_class(original_data_table_dict)
