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
    data_class = DataTableRepository.find(iteration, filename)
    if data_class:
        return data_class

    file_path = find_file(filename)
    data_class = DataTable.find_reference(file_path, fieldname, fieldvalue)
    DataTable.save(iteration, filename, data_class)
    return data_class

@keyword("Guardar Datos De Ejecucion")
def create_tests_results(iteration: int):
    BASE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "output", "results"
        )
    )

    files = [os.path.join(BASE_DIR, file) for file in os.listdir(BASE_DIR)]
    file = max(files, key=os.path.getctime)
    DataTable.create_output(file, iteration)
