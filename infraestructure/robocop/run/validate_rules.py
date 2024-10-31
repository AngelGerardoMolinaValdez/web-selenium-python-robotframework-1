import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validations.UseCasesRulesValidator import UseCasesRulesValidator
from validations.ScenariosRulesValidator import ScenariosRulesValidator
from validations.TestsRulesValidator import TestsRulesValidator

def main():
    components_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "components"))
    execution_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "execution"))
    rules_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules"))

    
    print(" USECASES ".center(110, "*"))
    usecases_validator = UseCasesRulesValidator(components_path, rules_path)
    usecases_validator.validate()
    print("\n" * 2)

    print(" SCENARIOS ".center(110, "*"))
    scenarios_validator = ScenariosRulesValidator(components_path, rules_path)
    scenarios_validator.validate()
    print("\n" * 2)

    print(" TESTS ".center(110, "*"))
    tests_validator = TestsRulesValidator(execution_path, rules_path)
    tests_validator.validate()
    print("\n" * 2)

if __name__ == "__main__":
    main()
