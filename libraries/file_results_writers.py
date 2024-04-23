from enum import Enum
import csv
import json
import os

class CsvResultWriter:
    @staticmethod
    def write(file_path, test_data, encoding):
        try:
            with open(file_path, mode='r', newline='', encoding=encoding) as f:
                lector = csv.reader(f)
                campos_existentes = next(lector, [])
        except FileNotFoundError:
            campos_existentes = []

        campos_nuevos = set(test_data.keys()) - set(campos_existentes)
        campos_actualizados = campos_existentes + list(campos_nuevos)

        if campos_nuevos:
            archivo_temporal = file_path + '.tmp'
            
            with open(archivo_temporal, mode='w', newline='', encoding=encoding) as f_temp:
                escritor = csv.DictWriter(f_temp, fieldnames=campos_actualizados)
                escritor.writeheader()

                if campos_existentes:
                    with open(file_path, mode='r', newline='', encoding=encoding) as f_orig:
                        lector = csv.DictReader(f_orig)
                        for fila in lector:
                            escritor.writerow(fila)
                
                escritor.writerow(test_data)

            os.replace(archivo_temporal, file_path)
        else:
            with open(file_path, mode='a', newline='', encoding=encoding) as f:
                escritor = csv.DictWriter(f, fieldnames=campos_existentes)
                if not campos_existentes:
                    escritor.writeheader()
                escritor.writerow(test_data)

class JsonResultWriter:
    @staticmethod
    def write(file_path, test_data, encoding):
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data_list = json.load(f)  # Cargar el archivo JSON existente
        except FileNotFoundError:
            data_list = []  # Inicializar una lista vacía si el archivo no existe

        if not data_list:
            # Si la lista está vacía, simplemente agregamos los datos nuevos
            data_list.append(test_data)
        else:
            # Encontrar todos los campos existentes en el JSON
            existing_fields = set()
            for item in data_list:
                existing_fields.update(item.keys())

            # Encontrar campos nuevos en los datos de entrada
            new_fields = set(test_data.keys()) - existing_fields

            # Agregar nuevos campos a cada registro existente, inicializados a None
            for item in data_list:
                for field in new_fields:
                    if field not in item:
                        item[field] = None  # O un valor predeterminado adecuado

            # Agregar el nuevo registro asegurándose que todos los campos estén presentes
            for field in existing_fields:
                if field not in test_data:
                    test_data[field] = None  # O un valor predeterminado adecuado
            data_list.append(test_data)

        # Escribir los datos actualizados en el archivo JSON
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)



class ResultWriterType(Enum):
    CSV = CsvResultWriter
    JSON = JsonResultWriter
