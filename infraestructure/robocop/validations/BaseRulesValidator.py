from abc import ABC, abstractmethod
import robocop

class BaseRulesValidator(ABC):
    def __init__(self, rules: set[str]):
        self.rules = rules

    @abstractmethod
    def _get_files(self):
        pass

    def validate(self):
        files = self._get_files()

        if not files:
            print("No files found")
            return

        config = robocop.Config()
        config.ext_rules = self.rules
        config.paths = files

        robocop_runner = robocop.Robocop(config=config)
        robocop_runner.reload_config()
        robocop_runner.run()
