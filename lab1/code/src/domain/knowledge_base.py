from lab1.code.src.domain.fact import Fact
from lab1.code.src.domain.rule import Rule


class KnowledgeBase:
    def __init__(self):
        self._rules = []
        self._facts: dict[str, Fact] = {}

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def delete_rule(self, index: int) -> None:
        self._rules.pop(index)

    def save_fact(self, fact_name: str, fact: Fact) -> None:
        self._facts[fact_name] = fact

    def remove_fact(self, fact_name: str) -> None:
        if fact_name in self._facts:
            del self._facts[fact_name]
        else:
            raise KeyError(f"Факт '{fact_name}' не найден")

    @property
    def rules(self) -> list[Rule]:
        return self._rules

    @property
    def facts(self) -> dict[str, Fact]:
        return self._facts
