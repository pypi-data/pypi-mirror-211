from gadapt.exit_check.base_exit_checker import BaseExitChecker

class RequestedCostExitChecker(BaseExitChecker):
    def __init__(self, requested_cost: float) -> None:
        super().__init__(1)
        self.requested_cost = requested_cost

    def is_exit(self, population):
        if population.min_cost <= self.requested_cost:
            return True
        return False