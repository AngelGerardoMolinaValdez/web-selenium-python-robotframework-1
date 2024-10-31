from robot.api.deco import keyword

class DictDataSetMerger:
    @keyword("Merge DataSets", tags=["library", "dataset-merger"])
    def merge_datasets(self, **datasets) -> dict:
        merged_dict = {}

        for _, dataset in datasets.items():
            for key, value in dataset.items():
                merged_dict[key] = value

        return merged_dict
