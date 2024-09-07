from robot.api.deco import keyword

class DictDataSetMerger:
    @keyword("Merge DataSets", tags=["library", "dataset-merger"])
    def merge_datasets(self, **datasets) -> dict:
        merged_dict = {}

        for dataset_name, dataset in datasets.items():
            for key, value in dataset.items():
                combined_key = f"{dataset_name}.{key}"
                merged_dict[combined_key] = value

        return merged_dict
