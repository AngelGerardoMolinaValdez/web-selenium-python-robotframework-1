import csv
import os
from robot.api.deco import keyword

class FileStateTracker:
    created_files = set()

    @classmethod
    def file_exists(self, file_path: str) -> bool:
        return file_path in self.created_files

    @classmethod
    def mark_file_created(self, file_path: str):
        self.created_files.add(file_path)


class DictDataSetSaver:
    @keyword("Save DataSet Results", tags=["library", "dataset-merger"])
    def save_dataset_results(self, dataset: dict, file_path: str):
        try:
            file_exists = FileStateTracker.file_exists(file_path)

            with open(file_path, mode="a" if file_exists else "w", newline="") as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(dataset.keys())

                writer.writerow(dataset.values())

            if not file_exists:
                FileStateTracker.mark_file_created(file_path)

        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")
