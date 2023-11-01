from dataclasses import dataclass

class DataTableRepository:
    """
    __data_tables = {
        0: [ <- seria la iteración
            { 
                "id": "general.data.csv", <- el nombre del archivo buscado
                "data": "" <- la dataclass
            },
            {
                "id": "general2.data.csv", <- el nombre del archivo buscado
                "data": "" <- la dataclass
            }
        ]
    }
    Se guarda asi porque la iteración durante una ejecución
    es constante y esto ayuda a que no se generen nuevas
    instancias de dataclass cuando se quiere obtener la misma
    dataclass según el nombre
    """
    __data_tables: dict = {}

    @classmethod
    def save(cls, iteration: int, name: str, data_class: dataclass):
        dataclass_iteration = cls.__data_tables.get(iteration)
        if dataclass_iteration is None:
            cls.__data_tables[iteration] = [
                {
                    "id": name,
                    "data": data_class
                }
            ]
            return 
        cls.__data_tables[iteration].append(
            {
                "id": name,
                "data": data_class
            }
        )

    @classmethod
    def find(cls, iteration: int, filename: str):
        data_info = cls.__data_tables.get(iteration)
        if data_info is None:
            return

        data_class_info = list(filter(
            lambda data_class: data_class["id"] == filename,
            data_info
        ))
        if data_class_info:
            return data_class_info[0]["data"]

    @classmethod
    def find_all(cls):
        return cls.__data_tables

    @classmethod
    def update(cls, data_class, new_data_class, iteration):
        data_classes_info = cls.__data_tables.get(iteration)

        for index, data_class_info in enumerate(data_classes_info):
            if id(data_class_info["data"]) == id(data_class):
                cls.__data_tables[iteration][index]["data"] = new_data_class
                break
