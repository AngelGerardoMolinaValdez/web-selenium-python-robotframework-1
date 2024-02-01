import csv
import json
import yaml
import pandas as pd


class FileDataReader:
    """A class to read data from different file formats
    
    Attributes
    ----------
    file_path : str
        The path of the file to read
    
    Methods
    -------
    read_json()
        Read a json file and return its data

    read_csv()
        Read a csv file and return its data

    read_excel()
        Read an excel file and return its data

    read_yaml()
        Read a yaml file and return its data
    
    Examples In Robot Framework
    ---------------------------

    *** Settings ***
    Library  libraries/FileDataReader.py

    *** Test Cases ***
    Read Json File
        ${data}=  Read Json  ${CURDIR}/data.json
        Log  ${data}    
    
    Read Csv File
        ${data}=  Read Csv  ${CURDIR}/data.csv
        Log  ${data}
    
    Read Excel File
        ${data}=  Read Excel  ${CURDIR}/data.xlsx
        Log  ${data}

    Read Yaml File 
        ${data}=  Read Yaml  ${CURDIR}/data.yaml
        Log  ${data}
    """

    @staticmethod
    def read_json(file_path) -> list[dict[str, str]]:
        """Read a json file and return its data as a list of dictionaries
        
        Example Input:
        [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        
        Example Output:
        [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        """
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def read_csv(file_path) -> list[dict[str, str]]:
        """Read a csv file and return its data as a list of dictionaries
        
        Example Input:
        name,age
        John,30
        Jane,25

        Example Output:
        [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        """
        data = []
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def read_excel(file_path, sheet_name="Datos") -> list[dict[str, str]]:
        """Read an excel file and return its data as a list of dictionaries
        
        Example Input:
        | name | age |
        |------|-----|
        | John | 30  |
        | Jane | 25  |

        Example Output:
        [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        """
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        return data.to_dict('records')

    @staticmethod
    def read_yaml(file_path) -> list[dict[str, str]]:
        """Read a yaml file and return its data as a list of dictionaries

        Example Input:
        - name: John
          age: 30
        - name: Jane
          age: 25
        
        Example Output:
        [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        """
        with open(file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
        return data
