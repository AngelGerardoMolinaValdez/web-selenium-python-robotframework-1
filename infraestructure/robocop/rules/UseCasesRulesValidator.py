import re
from robocop.checkers import VisitorChecker
from robocop.rules import Rule, RuleSeverity
from robot.api.parsing import Arguments

rules = {
    "9801": Rule(
        rule_id="9801", name="usecases-should-have-two-args", msg="El scenario debe tener dos argumentos: ${config} y ${reporters}.", severity=RuleSeverity.WARNING
    ),
    "9802": Rule(
        rule_id="9802", name="usecases-should-have-two-args-with-specific-naming", msg="El scenario debe tener los argumentos ${config} y ${reporters} y este tiene {{args}}", severity=RuleSeverity.WARNING
    ),
    "9803": Rule(
        rule_id="9803", name="usecases-should-not-import-usecases", msg="Los scenarios no pueden importar nada de pages/ de cualquier modulo", severity=RuleSeverity.WARNING
    ),
    "9804": Rule(
        rule_id="9804", name="usecases-should-not-import-scenarios", msg="Los scenarios no pueden importar nada de otros scenarios de cualquier modulo", severity=RuleSeverity.WARNING
    )
}

class UseCasesRulesValidator(VisitorChecker):
    reports = ("usecases-should-have-two-args", "usecases-should-have-two-args-with-specific-naming", "usecases-should-not-import-usecases", "usecases-should-not-import-scenarios")
    usecases_import_pattern = r".*[\\\/]?.*[\\\/]usecases[\\\/].*"
    scenario_import_pattern = r".*[\\\/]?.*[\\\/]scenarios[\\\/].*"

    def visit_Keyword(self, node):
        args = []
        for child in node.body:
            if isinstance(child, Arguments):
                args = child.values
                break
        if len(args) != 2:
            self.report("usecases-should-have-two-args", node=child)
        if args != ('${data_set}', '${reporters}'):
            self.report("usecases-should-have-two-args-with-specific-naming", node=child, args=args)
    
    def visit_ResourceImport(self, node):
        is_import_page = self.__validate_import_pattern(self.usecases_import_pattern, node.name)
        if is_import_page:
            self.report("usecases-should-not-import-usecases", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("usecases-should-not-import-scenarios", node=node)

    def visit_VariablesImport(self, node):
        is_import_page = self.__validate_import_pattern(self.usecases_import_pattern, node.name)
        if is_import_page:
            self.report("usecases-should-not-import-usecases", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("usecases-should-not-import-scenarios", node=node)

    def visit_LibraryImport(self, node):
        is_import_page = self.__validate_import_pattern(self.usecases_import_pattern, node.name)
        if is_import_page:
            self.report("usecases-should-not-import-usecases", node=node)

        is_import_scenario = self.__validate_import_pattern(self.scenario_import_pattern, node.name)
        if is_import_scenario:
            self.report("usecases-should-not-import-scenarios", node=node)

    def __validate_import_pattern(self, pattern: str, text: str):
        return re.fullmatch(pattern, text)
