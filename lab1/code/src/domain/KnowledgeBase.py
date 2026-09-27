from lab1.code.src.domain.Fact import Fact
from lab1.code.src.domain.Rule import Rule


class KnowledgeBase:
    def __init__(self):
        self._rules = []
        self._facts = []

    def add_rule(self, rule:Rule):
        self._rules.append(rule)

    def delete_rule(self, index:int):
        self._rules.pop(index)

    def add_fact(self, fact:Fact):
        self._facts.append(fact)

    def remove_fact(self, index:int):
        self._facts.pop(index)

    @property
    def rules(self):
        return self._rules

    @property
    def facts(self):
        return self._facts
