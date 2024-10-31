import re
from robocop.checkers import VisitorChecker
from robocop.rules import Rule, RuleSeverity
from robot.api.parsing import Arguments

rules = {
    "9901": Rule(
        rule_id="9901", name="scenario-should-have-two-args", msg="El scenario debe tener dos argumentos: ${config} y ${reporters}.", severity=RuleSeverity.WARNING
    ),
    "9902": Rule(
        rule_id="9902", name="scenario-should-have-two-args-with-specific-naming", msg="El scenario debe tener los argumentos ${config} y ${reporters} y este tiene {{args}}", severity=RuleSeverity.WARNING
    ),
    "9903": Rule(
        rule_id="9903", name="scenario-should-not-import-pages", msg="Los scenarios no pueden importar nada de pages/ de cualquier modulo", severity=RuleSeverity.WARNING
    ),
    "9904": Rule(
        rule_id="9904", name="scenario-should-not-import-scenarios", msg="Los scenarios no pueden importar nada de otros scenarios de cualquier modulo", severity=RuleSeverity.WARNING
    )
}

class ScenarioRulesValidator(VisitorChecker):
    reports = ("scenario-should-have-two-args", "scenario-should-have-two-args-with-specific-naming", "scenario-should-not-import-pages", "scenario-should-not-import-scenarios")
    page_import_pattern = r".*[\\\/]?.*[\\\/]pages[\\\/].*"
    scenario_import_pattern = r".*[\\\/]?.*[\\\/]scenarios[\\\/].*"

    def visit_Keyword(self, node):
        args = []
        for child in node.body:
            if isinstance(child, Arguments):
                args = child.values
                break
        if len(args) != 2:
            self.report("scenario-should-have-two-args", node=child)
        if args != ('${config}', '${reporters}'):
            self.report("scenario-should-have-two-args-with-specific-naming", node=child, args=args)
    
    def visit_ResourceImport(self, node):
        is_import_page = self.__validate_import_pattern(self.page_import_pattern, node.name)
        if is_import_page:
            self.report("scenario-should-not-import-pages", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("scenario-should-not-import-scenarios", node=node)

    def visit_VariablesImport(self, node):
        is_import_page = self.__validate_import_pattern(self.page_import_pattern, node.name)
        if is_import_page:
            self.report("scenario-should-not-import-pages", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("scenario-should-not-import-scenarios", node=node)

    def visit_LibraryImport(self, node):
        is_import_page = self.__validate_import_pattern(self.page_import_pattern, node.name)
        if is_import_page:
            self.report("scenario-should-not-import-pages", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("scenario-should-not-import-scenarios", node=node)

    def __validate_import_pattern(self, pattern: str, text: str):
        return re.fullmatch(pattern, text)
