"""
Librería enfocada a la creación y manipulación de data tables.

Durante la ejecución de los casos de prueba se usan datos que interactúan con el sistema.
Si tenemos diferentes casos de prueba que usan diferentes datos el guardar dichos datos resulta complicado.

Esta librería permite a traves de un csv crear un objeto de tipo dataclass de python y centralizar la información en una sola variable.

Ejemplo:

Suponiendo que tenemos el siguiente csv:
data.csv
id,name,age
0,David,20
1,Abigail,26

De este archivos con esta librería podemos generar un objeto dataclass donde el nombre del campo seria la primer fila ya que son catalogados como los encabezados de los datos y el valor seria el indice de la fila que le indiquemos, por ejemplo:
| ${dt} = Crear DataTable   data.csv    0
Hecho esto podríamos acceder a cualquier valor con el encabezado:
| Log   ${dt.name}  # David

Al igual que la solución anterior, podríamos también guardar un dato especifico en la dataclass, por ejemplo:

Obtuvimos un folio y necesitamos guardarlo en la dataclass para su posterior consulta. Esta librería también se encarga de esto.

CONSIDERACIÓN: Los encabezados dentro del archivo de datos debe ser compatible con el naming convention de una variable en python, es decir que:

Esto es valido:
- NOMBRE_COMPLETO
- nombre

Pero esto no:
- "nombre completo"
- "iteracion - anterior"

"""
import os
from robot.api.deco import keyword, not_keyword
from datatable import DataTable
from datatable_repository import DataTableRepository
from datatable_errors import DataTableDoesNotExist

DATA_DIR: str = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "data"
    )
)

@not_keyword
def find_file(name: str):
    for root, _, files in os.walk(DATA_DIR):
        for file_name in files:
            if file_name == name:
                return os.path.join(root, file_name)

    raise DataTableDoesNotExist(f"No existe el archivo {name}")

@keyword("Crear DataTable")
def create_data_table(filename: str, iteration: int):
    """
    Crea una dataclass a partir del nombre y obtiene los valores del indice que se le indique.

    Archivo de prueba data.csv
    id,name,age
    0,David,20
    1,Abigail,26

    | ${dt} = Crear DataTable   data.csv    0
    | Log   ${dt.name}  # David

    El argumento filename no requiere la ruta completa solo el nombre del archivo
    ya que esta ruta es validada desde la carpeta ``base/data/steps/`` en base a esa carpeta se validan todos los csv que hayan
    """
    data_class = DataTableRepository.find(iteration, filename)
    if data_class:
        return data_class

    file_path = find_file(filename)
    data_class, _ = DataTable.create(file_path, iteration)
    DataTable.save(iteration, filename, data_class)
    return data_class

@keyword("Crear DataTable Por Referencia")
def create_data_table_for_ref(
    filename: str, iteration: int, fieldname: str, fieldvalue: str
):
    """
    Crea una dataclass a partir del nombre del campo de otra dataclass

    Archivo de prueba data.csv
    id,name,age
    0,David,20
    1,Abigail,26

    Archivo de prueba data2.csv
    name,employee_id,
    David,emp00000
    Abigail,emp00001

    | ${dt} = Crear DataTable   data.csv    0
    | ${dt2} = Crear DataTable Por Referencia   data2.csv    0   name    ${dt.name}
    | Log   ${dt2.employee_id}  # David
    """
    data_class = DataTableRepository.find(iteration, filename)
    if data_class:
        return data_class

    file_path = find_file(filename)
    data_class = DataTable.find_reference(file_path, fieldname, fieldvalue)
    DataTable.save(iteration, filename, data_class)
    return data_class

@keyword("Guardar Datos De Ejecucion")
def create_tests_results(iteration: int):
    """
    Guarda los datos de las dataclasses en el archivo generado para los resultados de los casos de prueba.

    Archivo de prueba data.csv
    id,name,age
    0,David,20
    1,Abigail,26

    Archivo de prueba data2.csv
    name,employee_id,
    David,emp00000
    Abigail,emp00001

    | ${dt} = Crear DataTable   data.csv    0
    | ${dt2} = Crear DataTable Por Referencia   data2.csv    0   name    ${dt.name}
    | Guardar Datos De Ejecucion    0

    TestResults(index).csv
    id,name,age,name,id_employee
    0,David,20,David,emp00000
    1,Abigail,26,Abigail,emp00001

    Si no se usa esta keyword los valores no serán guardados en el archivos de resultados creado
    """
    BASE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "output", "results"
        )
    )

    files = [os.path.join(BASE_DIR, file) for file in os.listdir(BASE_DIR)]
    file = max(files, key=os.path.getctime)
    DataTable.create_output(file, iteration)

@keyword("Guardar En DataTable")
def save_content(datatable: DataTable, iteration: int, fieldname: str, value: str):
    """
    Agrega un la dataclass que se especifique

    Archivo de prueba data.csv
    id,name,age
    0,David,20

    | ${dt} = Crear DataTable   data.csv    0
    | ${new_dt}   Guardar En DataTable  ${dt}   0   salary  20000
    | Guardar Datos De Ejecucion    0

    TestResults(index).csv
    id,name,salary,
    0,David,20,20000

    Las dataclasses son inmutables por lo que al agregar un valor a la dataclasses esta librería crea una nueva con los mismos valores pero agregando el nuevo por lo que
    si no se obtiene de los resultados de la keyword no podrá ver en su dataclass el nuevo campo durante la ejecución
    , sin embargo si se vera en los resultados finales
    """
    dt = DataTable.write_content(datatable, fieldname, value)
    DataTableRepository.update(datatable, dt, iteration)
    return dt
