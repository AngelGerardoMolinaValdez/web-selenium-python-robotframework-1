import sys
import os
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .BaseRulesValidator import BaseRulesValidator

class UseCasesRulesValidator(BaseRulesValidator):
    def __init__(self, components_path, rules_path: str):
        self.components_path = components_path
        rules = {os.path.join(rules_path, "UseCasesRulesValidator.py")}
        super().__init__(rules)

    def _get_files(self):
        scenarios_glob_pattern = os.path.join(self.components_path, "**", "usecases", "**", "*.resource")
        scenarios_files: list[str] = glob.glob(scenarios_glob_pattern, recursive=True)
        return scenarios_files
