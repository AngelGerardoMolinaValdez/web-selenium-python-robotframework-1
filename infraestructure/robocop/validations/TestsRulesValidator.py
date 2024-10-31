import sys
import os
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .BaseRulesValidator import BaseRulesValidator

class TestsRulesValidator(BaseRulesValidator):
    def __init__(self, execution_path, rules_path: str):
        self.execution_path = execution_path
        rules = {os.path.join(rules_path, "TestsRulesValidator.py")}
        super().__init__(rules)

    def _get_files(self):
        tests_glob_pattern = os.path.join(self.execution_path, "**", "tests", "**", "*.robot")
        tests_files: list[str] = glob.glob(tests_glob_pattern, recursive=True)
        return tests_files
