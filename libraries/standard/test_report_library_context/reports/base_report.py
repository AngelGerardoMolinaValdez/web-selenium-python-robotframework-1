from abc import ABC, abstractmethod

class BaseReport(ABC):
    @abstractmethod
    def create(self, test_name, status, steps, setup_steps, teardown_steps, base_path):
        pass
