import re
from robocop.checkers import VisitorChecker
from robocop.rules import Rule, RuleSeverity

rules = {
    "9701": Rule(
        rule_id="9701", name="tests-only-imports-scenarios-to-execute", msg="Los casos de deben importar solamente los escenarios de un bloque de negocio.", severity=RuleSeverity.WARNING
    )
}

class TestsRulesValidator(VisitorChecker):
    reports = ("tests-only-imports-scenarios-to-execute",)
    scenario_import_pattern = r".*[\\\/]?.*[\\\/]scenarios[\\\/].*"

    def visit_ResourceImport(self, node):
        is_not_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if not is_not_import_scenario:
            self.report("tests-only-imports-scenarios-to-execute", node=node)

    def __validate_import_pattern(self, pattern: str, text: str):
        return re.fullmatch(pattern, text)
