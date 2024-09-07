from typing import Any
from robot.api.deco import keyword

class DictDataSetUpdater:
    @keyword("Update DataSet", tags=["library", "dict-dataset-updater"])
    def update_dataset(self, dataset: dict, **fields) -> dict:
        for key, value in fields.items():
            dataset[key] = value
        return dataset
